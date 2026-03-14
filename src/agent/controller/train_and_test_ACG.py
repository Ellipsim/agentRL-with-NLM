"""
> train_and_test.py

Main script for training and testing the solver policy under ACL.

NOTE: This script should be executed as a module:
  python -m src.agent.controller.train_and_test

This script is intentionally thin. It is responsible for:
  1. Parsing and validating command-line arguments
  2. Setting up the experiment folder and policy
  3. Calling trainer.train_acl() — which owns the full training loop,
     periodic test evaluation, and experience replay
  4. Calling trainer.test() for the optional final test run

All loop logic (replay buffer, test curve, PPO updates, checkpointing)
lives in PolicyTrainer. See trainer.py for details.

Key differences from NeSIG:
  - Problems are SOLVED, not generated
  - Single policy (not init + goal)
  - No validation set, no best-model selection (only last.ckpt)
  - No consistency/difficulty/diversity evaluators
"""

import argparse
import hashlib
import os
import torch
from os.path import dirname, abspath
from pathlib import Path
from pytorch_lightning import seed_everything
import json
from typing import List, Optional, Tuple
from lifted_pddl import Parser
import random

from src.agent.constants import (
    EXPERIMENT_INFO_FILENAME, LOGS_FOLDER_NAME, CKPTS_FOLDER_NAME,
    TEST_FOLDER_NAME, remove_if_exists, EXCLUDED_ARGS_ID, ID_LENGTH,
    ADDITIONAL_EXPERIMENT_INFO,
)
from src.agent.learning.generative_policy import RandomPolicy, PPOSolverPolicy
from src.agent.learning.model_wrapper import NLMWrapperActor, NLMWrapperCritic
from src.agent.pddl.problem_solver import ProblemSolver
from src.agent.pddl.pddl_problem import PDDLProblem
from src.agent.pddl.pddl_state import PDDLState
from src.agent.controller.trainer import PolicyTrainer, ReplayBuffer, REPLAY_BUFFER_FILENAME


# =====================================================================
# Argument Parsing
# =====================================================================

def parse_max_actions(value):
    """Parse either a single integer or a comma-separated tuple of integers."""
    try:
        val = int(value)
        if val <= 0:
            raise argparse.ArgumentTypeError("Max actions must be > 0")
        return val
    except ValueError:
        pass
    try:
        parts = value.split(',')
        val = tuple(int(p) for p in parts)
        if any(v <= 0 for v in val):
            raise argparse.ArgumentTypeError("Max actions must be > 0")
        return val
    except ValueError:
        raise argparse.ArgumentTypeError("Max actions must be int or tuple of ints")


def parse_arguments():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Train and test a solver policy with ACL + experience replay.",
    )

    # ---- Domain / problems ----
    parser.add_argument('--domain-path', type=str, required=True,
                        help="Path to domain.pddl file")
    parser.add_argument('--generator-path', type=str, default='./problem_generator/pddl-generators/blocksworld/blocksworld',
                    help="Path to the blocksworld generator binary")
    parser.add_argument('--data-dir', type=str, default='./data/problems/curriculum',
                    help="Directory to store generated problems")
    
    # ---- Generator ----
    parser.add_argument('--min-blocks-start', type=int, default=2,
                    help="Minimum number of blocks at level 1")
    parser.add_argument('--max-blocks-start', type=int, default=3,
                        help="Maximum number of blocks at level 1")
    parser.add_argument('--blocks-increment', type=int, default=1,
                        help="How many blocks to add per level")
    parser.add_argument('--max-levels', type=int, default=4,
                        help="Number of curriculum levels")
    parser.add_argument('--advance-threshold', type=float, default=0.8,
                        help="Train success rate needed to advance to next level")
    parser.add_argument('--check-advance-period', type=int, default=10,
                        help="How often (in iterations) to check if ready to advance")
    parser.add_argument('--test-min-blocks', type=int, default=None,
                        help="Min blocks for test problems (default: level 1 min)")
    parser.add_argument('--test-max-blocks', type=int, default=None,
                        help="Max blocks for test problems (default: hardest level max)")

    # ---- Reproducibility ----
    parser.add_argument('--seed', type=int, default=1)
    parser.add_argument('--run-id', type=int, default=0,
                        help="Extra ID for repeated experiments with same arguments")

    # ---- Training ----
    parser.add_argument('--steps', type=int, default=100,
                        help="Total training iterations")
    parser.add_argument('--num-problems-train', type=int, default=5,
                        help="Problems per training iteration")
    parser.add_argument('--max-actions-train', type=parse_max_actions, default=None,
                        help="Action budget per training problem")
    parser.add_argument('--batch-size', type=int, default=32)
    parser.add_argument('--min-samples-train', type=int, default=10,
                        help="Min trajectory samples needed before a PPO update")
    parser.add_argument('--grad-clip', type=float, default=0.5,
                        help="Gradient clipping (-1 to disable)")
    parser.add_argument('--target-success-rate', type=float, default=1.0,
                    help="Stop training early if test success rate reaches this value.")

    # ---- Returns / advantages ----
    parser.add_argument('--disc-factor', type=float, default=0.99, help="Discount factor gamma")
    parser.add_argument('--gae-factor', type=float, default=0.95, help="GAE factor lambda")

    # ---- Periodic test evaluation ----
    parser.add_argument('--test-period', type=int, default=10,
                        help="Steps between test evaluations (-1 = only at the end). ")
    parser.add_argument('--num-problems-test', type=int, default=20,
                        help="Problems per test evaluation")
    parser.add_argument('--max-actions-test', type=parse_max_actions, default=None,
                        help="Action budget per test problem")

    # ---- Experience replay ----
    parser.add_argument('--replay-prob', type=float, default=0.2,
                        help="Probability of replacing a curriculum slot with a replayed "
                             "problem. Set 0.0 to disable.")
    parser.add_argument('--replay-buffer-size', type=int, default=3000,
                        help="Max problem paths kept in the replay buffer (FIFO eviction).")

    # ---- Logging ----
    parser.add_argument('--log-period', type=int, default=1,
                        help="Steps between TensorBoard logging")

    # ---- Device ----
    parser.add_argument('--device', type=str, choices=('gpu', 'cpu'), default='gpu')

    # ---- Run modes ----
    parser.add_argument('--train-mode', choices=('skip', 'supersede', 'resume'), default='resume')
    parser.add_argument('--test-mode', choices=('skip', 'supersede', 'missing'), default='missing',
                        help="Controls the optional final test run at the end of training. "
                             "Periodic evaluations are always written regardless of this flag.")
    parser.add_argument('--raise-error-test', action='store_true',
                        help="Raise error if final test attempted without a trained policy")

    # ---- Experiment folder ----
    parser.add_argument('--experiments-dir', type=str, default='./experiments')

    # ---- Policy type ----
    parser.add_argument('--policy-type', choices=('random', 'PPO'), default='PPO')

    # ---- Rewards ----
    parser.add_argument('--reward-goal-reached', type=float, default=1.0)
    parser.add_argument('--reward-step', type=float, default=-0.01)
    parser.add_argument('--reward-efficiency', type=float, default=0.5)

    # ---- NLM model args ----
    NLMWrapperActor.add_model_specific_args(parser)
    parser.add_argument('--critic-loss-weight', type=float, default=0.1)

    # ---- PPO policy args ----
    PPOSolverPolicy.add_model_specific_args(parser)

    return parser.parse_args()


def validate_args(args):
    if args.steps < 1:
        raise ValueError("--steps must be > 0")
    if args.max_levels < 1:
        raise ValueError("--max-levels must be > 0")
    if not (0 < args.advance_threshold <= 1):
        raise ValueError("--advance-threshold must be in (0, 1]")
    if args.min_blocks_start < 2:
        raise ValueError("--min-blocks-start must be >= 2")
    if args.max_blocks_start < args.min_blocks_start:
        raise ValueError("--max-blocks-start must be >= --min-blocks-start")
    if args.blocks_increment < 1:
        raise ValueError("--blocks-increment must be >= 1")
    if args.batch_size < 1:
        raise ValueError("--batch-size must be > 0")
    if args.min_samples_train < 1:
        raise ValueError("--min-samples-train must be > 0")
    if not 0.0 <= args.disc_factor <= 1.0:
        raise ValueError("--disc-factor must be in [0, 1]")
    if not 0.0 <= args.gae_factor <= 1.0:
        raise ValueError("--gae-factor must be in [0, 1]")
    if not 0.0 <= args.replay_prob <= 1.0:
        raise ValueError("--replay-prob must be in [0, 1]")
    if args.replay_buffer_size < 1:
        raise ValueError("--replay-buffer-size must be > 0")
    if args.train_mode == "skip" and args.test_mode == "skip":
        raise ValueError("Cannot skip both training and testing")

    args.domain_path = str(Path(args.domain_path).resolve())
    args.generator_path = str(Path(args.generator_path).resolve())
    args.data_dir = str(Path(args.data_dir).resolve())

    if not Path(args.domain_path).exists():
        raise ValueError(f"Domain file not found: {args.domain_path}")
    if not Path(args.generator_path).exists():
        raise ValueError(f"Generator not found: {args.generator_path}")

    if args.grad_clip == -1:
        args.grad_clip = None
    elif args.grad_clip <= 0:
        raise ValueError("--grad-clip must be > 0 or -1")

    # Resolve block ranges 
    if args.test_min_blocks is None:
        args.test_min_blocks = args.min_blocks_start
    if args.test_max_blocks is None:
        args.test_max_blocks = args.max_blocks_start + (args.max_levels - 1) * args.blocks_increment

    # Resolve max_actions
    if args.max_actions_train is None:
        max_blocks_train = args.max_blocks_start + (args.max_levels - 1) * args.blocks_increment
        args.max_actions_train = 4 * (max_blocks_train - 1)
    if args.max_actions_test is None:
        args.max_actions_test = 4 * (args.test_max_blocks - 1)

    return args


def get_level_blocks(args, level: int) -> Tuple[int, int]:
    """Get min/max blocks for a given curriculum level."""
    min_blocks = args.min_blocks_start + (level - 1) * args.blocks_increment
    max_blocks = args.max_blocks_start + (level - 1) * args.blocks_increment
    return min_blocks, max_blocks


def generate_problems(generator_path: str, out_dir: str,
                      count: int, min_blocks: int, max_blocks: int,
                      seed_start: int = 0) -> None:
    """Generate PDDL problems using the blocksworld generator binary."""
    import subprocess
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    for f in out_path.glob("*.pddl"):
        f.unlink()

    print(f"    Generating {count} problems ({min_blocks}-{max_blocks} blocks) -> {out_dir}")

    for i in range(count):
        blocks = random.randint(min_blocks, max_blocks)
        seed = seed_start + i
        out_file = out_path / f"problem_{i + 1}.pddl"

        result = subprocess.run(
            [generator_path, '4', str(blocks), str(seed)],
            capture_output=True, text=True
        )

        if result.returncode != 0:
            raise RuntimeError(f"Generator failed for problem {i + 1}: {result.stderr}")

        out_file.write_text(result.stdout)

# =====================================================================
# Experiment Management
# =====================================================================

def get_experiment_id(args):
    included = {k: v for k, v in vars(args).items() if k not in EXCLUDED_ARGS_ID}
    return hashlib.sha256(str(included).encode()).hexdigest()[:ID_LENGTH]


def save_experiment_info(filepath, args, experiment_id, last_train_it):
    """Persist experiment metadata.
    No best_train_it / best_val_score — no validation phase, model never rolled back.
    """
    info = {k: v for k, v in vars(args).items() if k not in EXCLUDED_ARGS_ID}
    info['experiment_id'] = experiment_id
    info['last_train_it'] = last_train_it
    info.update(ADDITIONAL_EXPERIMENT_INFO)
    with open(filepath, 'w') as f:
        json.dump(info, f, indent=2)


def read_last_train_it(experiment_info_path: Path) -> int:
    if experiment_info_path.exists():
        with open(experiment_info_path) as f:
            return json.load(f).get('last_train_it', 0)
    return 0


# =====================================================================
# Problem Loading
# =====================================================================

def load_problems_from_dir(
    problem_dir,
    domain_path,
    num_problems,
    max_actions=None,
    replay_buffer: Optional[ReplayBuffer] = None,
    replay_prob: float = 0.0,
) -> List[PDDLProblem]:
    import random
    problem_dir = Path(problem_dir)
    problem_files = sorted(problem_dir.glob("*.pddl"))
    if not problem_files:
        raise FileNotFoundError(f"No .pddl files in {problem_dir}")

    problems = []
    for i in range(num_problems):
        use_replay = (
            replay_buffer is not None
            and len(replay_buffer) > 0
            and random.random() < replay_prob
        )
        path = replay_buffer.sample() if use_replay else str(problem_files[i % len(problem_files)])

        fresh_parser = Parser()
        fresh_parser.parse_domain(str(domain_path))
        problem = PDDLProblem.load_from_pddl(fresh_parser, path)

        if problem is not None:
            if max_actions is not None:
                problem.max_actions = (
                    max_actions[i % len(max_actions)]
                    if isinstance(max_actions, tuple)
                    else max_actions
                )
            problems.append(problem)

    # Register AFTER sampling so current level never appears in replay slots
    if replay_buffer is not None:
        replay_buffer.register_dir(str(problem_dir))

    return problems


# =====================================================================
# Policy Creation
# =====================================================================

def create_policy(args, parser, last_train_it, experiment_folder_path, device):
    """Create or load policy."""
    if args.policy_type == 'random':
        return RandomPolicy()
    
    elif args.policy_type == 'PPO':
        # Create actor/critic for solver
        # NLM needs actions to be treated as predicates (NeSIG legacy)
        # TODO: Is there a better way to do this?
        domain_actions = set([
        (action[0], tuple([var for var, var_class in zip(action[1][0], action[1][1]) if var_class=='param']))
        for action in parser.actions])

        dummy_state = PDDLState(
            types=parser.types,
            type_hierarchy=parser.type_hierarchy,
            predicates=domain_actions,  # Actions as predicates!
            objects=[],
            atoms=set()
        )
        
        # Convert args to dict for NLMWrapper (it expects dict with specific keys)
        args_dict = vars(args)
        
        actor_args = {'dummy_pddl_state': dummy_state}
        critic_args = {'dummy_pddl_state': dummy_state}
        
        # Load or create policy
        if args.train_mode == "supersede" or last_train_it == 0:
            policy = PPOSolverPolicy(
                args=args_dict,  # Pass as dict
                actor_class=NLMWrapperActor,
                actor_arguments=actor_args,
                critic_class=NLMWrapperCritic,
                critic_arguments=critic_args,
                device=device
            )
        elif args.train_mode in ("resume", "skip"):
            ckpt_path = experiment_folder_path / CKPTS_FOLDER_NAME / 'last.ckpt'
            # Create fresh policy, then load saved state
            policy = PPOSolverPolicy(
                args=args_dict,
                actor_class=NLMWrapperActor,
                actor_arguments=actor_args,
                critic_class=NLMWrapperCritic,
                critic_arguments=critic_args,
                device=device
            )
            checkpoint = torch.load(str(ckpt_path), map_location=device)
            policy.load_state_dict(checkpoint['state_dict'])
        else:
            raise ValueError(f"Invalid train_mode: {args.train_mode}")
        
        return policy
    
    else:
        raise ValueError(f"Unknown policy type: {args.policy_type}")


# =====================================================================
# Training
# =====================================================================

def train(args, parser, experiment_id, experiment_folder_path: Path):
    experiment_info_path = experiment_folder_path / EXPERIMENT_INFO_FILENAME
    experiment_folder_path.mkdir(parents=True, exist_ok=True)

    last_train_it = read_last_train_it(experiment_info_path)
    print(f"Previous progress: last_train_it={last_train_it}")

    if args.train_mode == 'supersede' or last_train_it == 0:
        for folder in (LOGS_FOLDER_NAME, CKPTS_FOLDER_NAME, TEST_FOLDER_NAME):
            remove_if_exists(experiment_folder_path / folder)
        p = experiment_folder_path / REPLAY_BUFFER_FILENAME
        if p.exists():
            p.unlink()
        last_train_it = 0
        # Clear all previously generated curriculum problems
        data_dir = Path(args.data_dir)
        if data_dir.exists():
            import shutil
            shutil.rmtree(data_dir)
            data_dir.mkdir(parents=True, exist_ok=True)

    save_experiment_info(experiment_info_path, args, experiment_id, last_train_it)

    if args.train_mode == 'skip' or args.policy_type == 'random':
        return
    if last_train_it >= args.steps:
        print("Training already complete.")
        return

    # --- Generate fixed test set once ---
    test_problems_dir = Path(args.data_dir) / 'test'
    if not test_problems_dir.exists() or not list(test_problems_dir.glob('*.pddl')):
        print("\nGenerating fixed test set...")
        generate_problems(
            args.generator_path, str(test_problems_dir),
            args.num_problems_test,
            args.test_min_blocks, args.test_max_blocks,
            seed_start=999454,
        )

    # Load test problems
    test_problems = load_problems_from_dir(
        str(test_problems_dir), args.domain_path,
        args.num_problems_test,
        max_actions=args.max_actions_test,
    )

    # --- Set up replay buffer, policy, solver, trainer ---
    replay_buffer = ReplayBuffer(max_size=args.replay_buffer_size)
    replay_buffer.load(experiment_folder_path)

    device = torch.device('cuda' if args.device == 'gpu' else 'cpu')
    policy = create_policy(args, parser, last_train_it, experiment_folder_path, device)
    problem_solver = ProblemSolver(
        parser, policy,
        reward_goal_reached=args.reward_goal_reached,
        reward_step=args.reward_step,
        reward_efficiency=args.reward_efficiency,
    )
    trainer = PolicyTrainer(args, experiment_folder_path, problem_solver, policy, device)

    if device.type == 'cuda':
        policy.to('cuda')

    print(f"\n{'='*70}")
    print(f"TRAINING  (ACL + curriculum + replay)")
    print(f"Steps : {last_train_it + 1} -> {args.steps}")
    print(f"Replay: prob={args.replay_prob}  buffer={args.replay_buffer_size}")
    print(f"Test  : every {args.test_period} steps  ({args.num_problems_test} problems)")
    print(f"{'='*70}\n")

    current_step = last_train_it + 1

    

    # --- Curriculum loop ---
    for level in range(1, args.max_levels + 1):
        if current_step > args.steps:
            break

        min_blocks, max_blocks = get_level_blocks(args, level)
        level_train_dir = Path(args.data_dir) / f'level_{level}' / 'train'

        print(f"\n[LEVEL {level}/{args.max_levels}  {min_blocks}-{max_blocks} blocks]")

        generate_problems(
            args.generator_path,
            str(level_train_dir),
            args.num_problems_train,
            min_blocks,
            max_blocks,
            seed_start=current_step * 1000 + level,
        )

        train_problems = load_problems_from_dir(
            str(level_train_dir),
            args.domain_path,
            args.num_problems_train,
            max_actions=args.max_actions_train,
            replay_buffer=replay_buffer,
            replay_prob=args.replay_prob,
        )

        # Register buffer
        replay_buffer.register_dir(str(level_train_dir))

        current_step, level_beaten, target_reached = trainer.train_acl_level(
            problems=train_problems,
            test_problems=test_problems,
            start_step=current_step,
            max_steps=args.steps,
            target_success_rate=args.target_success_rate,
        )

        # Log curriculum level
        trainer.log_curriculum_level(level, current_step)

        replay_buffer.save(experiment_folder_path)
        save_experiment_info(experiment_info_path, args, experiment_id, current_step - 1)

        if target_reached:
            print(f"\n  Target success rate reached. Stopping training.")
            break

        if not level_beaten:
            print(f"\n  Steps exhausted at level {level}/{args.max_levels}.")
            break

        print(f"\n  ✓ Level {level} beaten. Advancing...")

        if level == args.max_levels:
            print(f"  Max level reached. Continuing on level {level} until steps run out...")
            while current_step <= args.steps:
                train_problems = load_problems_from_dir(
                    str(level_train_dir),
                    args.domain_path,
                    args.num_problems_train,
                    max_actions=args.max_actions_train,
                    replay_buffer=replay_buffer,
                    replay_prob=args.replay_prob, 
                )

                current_step, _, target_reached = trainer.train_acl_level(
                    problems=train_problems,
                    test_problems=test_problems,
                    start_step=current_step,
                    max_steps=args.steps,
                    target_success_rate=args.target_success_rate,
                )

                trainer.log_curriculum_level(level, current_step)
                replay_buffer.save(experiment_folder_path)
                save_experiment_info(experiment_info_path, args, experiment_id, current_step - 1)
                if target_reached:
                    print(f"\n  Target success rate reached. Stopping training.")
                    break

    trainer.close_writers()
    print(f"\n{'='*70}")
    print(f"Training complete.")
    print(f"{'='*70}\n")


# =====================================================================
# Final Test Run
# =====================================================================

def run_final_test(args, parser, experiment_id, experiment_folder_path: Path):
    """Optional final test run using the last checkpoint.

    The periodic evaluations in test_curve.json are the primary signal;
    this is a convenience run for a clean end-of-training result.
    """
    if args.test_mode == 'skip':
        return

    experiment_info_path = experiment_folder_path / EXPERIMENT_INFO_FILENAME
    test_folder_path = experiment_folder_path / TEST_FOLDER_NAME

    if args.policy_type != 'random':
        ckpt_path = experiment_folder_path / CKPTS_FOLDER_NAME / 'last.ckpt'
        if not ckpt_path.exists():
            if args.raise_error_test:
                raise FileNotFoundError(f"Checkpoint not found: {ckpt_path}")
            print("Skipping final test: no trained policy found.")
            return

    if args.test_mode == 'supersede':
        remove_if_exists(test_folder_path)
    test_folder_path.mkdir(parents=True, exist_ok=True)

    device = torch.device('cuda' if args.device == 'gpu' else 'cpu')
    last_train_it = read_last_train_it(experiment_info_path)
    policy = create_policy(
        args, 
        parser, 
        last_train_it, 
        experiment_folder_path, 
        device
    )
    if args.policy_type != 'random':
        checkpoint = torch.load(str(ckpt_path), map_location=device)
        policy.load_state_dict(checkpoint['state_dict'])

    problem_solver = ProblemSolver(
        parser, 
        policy,
        reward_goal_reached=args.reward_goal_reached,
        reward_step=args.reward_step,
        reward_efficiency=args.reward_efficiency,
    )
    trainer = PolicyTrainer(args, experiment_folder_path, problem_solver, policy, device)

    test_problems_dir = Path(args.data_dir) / 'test'
    def get_test_problems():
        return load_problems_from_dir(
            str(test_problems_dir), 
            args.domain_path, 
            args.num_problems_test,
            max_actions=args.max_actions_test,
        )

    trainer.test(test_problems_fn=get_test_problems)


# =====================================================================
# Entry Point
# =====================================================================

def main(args):
    os.chdir(dirname(dirname(dirname(dirname(abspath(__file__))))))
    seed_everything(args.seed, workers=True)

    experiment_id = get_experiment_id(args)
    print(f"\n>>> Experiment ID: {experiment_id}\n")

    experiment_folder_path = Path(args.experiments_dir) / experiment_id

    parser = Parser()
    parser.parse_domain(args.domain_path)

    train(args, parser, experiment_id, experiment_folder_path)
    run_final_test(args, parser, experiment_id, experiment_folder_path)

    print("\n>>> Done!")
    print(f">>> Experiment ID: {experiment_id}\n")


if __name__ == '__main__':
    args = parse_arguments()
    args = validate_args(args)
    main(args)