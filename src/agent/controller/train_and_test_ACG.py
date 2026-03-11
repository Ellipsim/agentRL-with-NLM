"""
> train_and_test_curriculum.py

Main script for training with automatic curriculum learning.

NOTE: This script should be executed as a module:
  python -m src.agent.controller.train_and_test_curriculum

Curriculum workflow:
  1. Generate fixed test problems (once, hardest difficulty)
  2. For each curriculum level:
      a. Generate train+val problems matching current difficulty
      b. Train until val success rate >= advance_threshold OR max steps_per_level reached
      c. Advance to next level (harder problems)
  3. Test final policy on fixed test problems

Key differences from train_and_test.py:
  - Problems are generated on-the-fly via the blocksworld generator
  - Training loop is level-based instead of iteration-based
  - Val problems change with each level
  - Test problems are fixed (hardest difficulty, generated once)
  - Single policy is kept and trained across all levels
"""

import argparse
import hashlib
import subprocess
import sys
import os
import torch
import random
from os.path import dirname, abspath
from pathlib import Path
from pytorch_lightning import seed_everything
import json
from typing import Tuple, List, Dict, Optional
from lifted_pddl import Parser

from src.agent.constants import (
    EXPERIMENT_INFO_FILENAME, LOGS_FOLDER_NAME, CKPTS_FOLDER_NAME,
    VAL_FOLDER_NAME, TEST_FOLDER_NAME, remove_if_exists,
    EXCLUDED_ARGS_ID, ID_LENGTH, ADDITIONAL_EXPERIMENT_INFO
)
from src.agent.learning.generative_policy import GenerativePolicy, RandomPolicy, PPOSolverPolicy
from src.agent.learning.model_wrapper import NLMWrapperActor, NLMWrapperCritic
from src.agent.pddl.problem_solver import ProblemSolver
from src.agent.pddl.pddl_problem import PDDLProblem
from src.agent.pddl.pddl_state import PDDLState
from src.agent.controller.trainer import PolicyTrainer


# =====================================================================
# Argument Parsing
# =====================================================================

def parse_max_actions(value):
    """Parse either a single integer or tuple of integers."""
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

# TODO: Ya no hay límite de steps global, habría que agregarlo

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Train with automatic curriculum learning and test."
    )

    # ---- Domain configuration ----
    parser.add_argument(
        '--domain-path', type=str, required=True,
        help="Path to domain.pddl file"
    )
    parser.add_argument(
        '--generator-path', type=str, required=True,
        help="Path to the blocksworld generator binary"
    )
    parser.add_argument(
        '--data-dir', type=str, default='./data/problems/curriculum',
        help="Directory to store generated problems"
    )

    # ---- Curriculum configuration ----
    parser.add_argument(
        '--min-blocks-start', type=int, default=2,
        help="Minimum number of blocks at level 1"
    )
    parser.add_argument(
        '--max-blocks-start', type=int, default=3,
        help="Maximum number of blocks at level 1"
    )
    parser.add_argument(
        '--blocks-increment', type=int, default=1,
        help="How many blocks to add per level (min and max)"
    )
    parser.add_argument(
        '--max-levels', type=int, default=4,
        help="Number of curriculum levels"
    )
    parser.add_argument(
        '--advance-threshold', type=float, default=0.8,
        help="Val success rate needed to advance to next level"
    )
    parser.add_argument(
        '--steps-per-level', type=int, default=100, # default is no limit 
        help="Max training iterations per curriculum level"
    )
    parser.add_argument(
        '--check-advance-period', type=int, default=10,
        help="How often (in iterations) to check if ready to advance"
    )

    # ---- Problem generation configuration ----
    parser.add_argument(
        '--num-problems-train', type=int, default=30,
        help="Number of training problems per level"
    )
    parser.add_argument(
        '--num-problems-val', type=int, default=30,
        help="Number of validation problems per level"
    )
    parser.add_argument(
        '--num-problems-test', type=int, default=100,
        help="Number of test problems (fixed, hardest difficulty)"
    )
    parser.add_argument(
        '--test-min-blocks', type=int, default=None,
        help="Min blocks for test problems (default: hardest level min)"
    )
    parser.add_argument(
        '--test-max-blocks', type=int, default=None,
        help="Max blocks for test problems (default: hardest level max)"
    )

    # ---- Action budgets ----
    parser.add_argument(
        '--max-actions-train', type=parse_max_actions, default=50,
        help="Action budget per training problem"
    )
    parser.add_argument(
        '--max-actions-val', type=parse_max_actions, default=50,
        help="Action budget per validation problem"
    )
    parser.add_argument(
        '--max-actions-test', type=parse_max_actions, default=100,
        help="Action budget per test problem"
    )

    # ---- Reproducibility ----
    parser.add_argument(
        '--seed', type=int, default=1,
        help="Random seed for reproducibility"
    )
    parser.add_argument(
        '--run-id', type=int, default=0,
        help="Extra ID for repeated experiments with same arguments"
    )

    # ---- PPO Training configuration ----
    parser.add_argument(
        '--batch-size', type=int, default=32,
        help="Minibatch size during PPO training"
    )
    parser.add_argument(
        '--min-samples-train', type=int, default=10,
        help="Min samples needed to perform PPO update"
    )
    parser.add_argument(
        '--grad-clip', type=float, default=0.5,
        help="Gradient clipping value (use -1 for no clipping)"
    )
    parser.add_argument(
        '--disc-factor', type=float, default=0.99,
        help="Discount factor (gamma) for returns"
    )
    parser.add_argument(
        '--gae-factor', type=float, default=0.95,
        help="GAE factor (lambda) for advantage estimation"
    )

    # ---- Logging ----
    parser.add_argument(
        '--log-period', type=int, default=1,
        help="Training steps between logging"
    )

    # ---- Device ----
    parser.add_argument(
        '--device', type=str, choices=('gpu', 'cpu'), default='gpu',
        help="Device for training"
    )

    # ---- Training/Test modes ----
    parser.add_argument(
        '--train-mode', choices=('skip', 'supersede', 'resume'), default='resume',
        help="Training mode: skip/supersede/resume"
    )
    parser.add_argument(
        '--test-mode', choices=('skip', 'supersede', 'missing'), default='missing',
        help="Testing mode: skip/supersede/missing"
    )

    # ---- Experiment management ----
    parser.add_argument(
        '--experiments-dir', type=str, default='./experiments',
        help="Directory to save experiments"
    )

    # ---- Policy type ----
    parser.add_argument(
        '--policy-type', choices=('random', 'PPO'), default='PPO',
        help="Policy type: random or PPO"
    )

    # ---- Reward configuration ----
    parser.add_argument(
        '--reward-goal-reached', type=float, default=1.0,
        help="Reward bonus when goal is reached"
    )
    parser.add_argument(
        '--reward-step', type=float, default=-0.01,
        help="Penalty for each step"
    )
    parser.add_argument(
        '--reward-efficiency', type=float, default=0.5,
        help="Weight for efficiency bonus"
    )

    # ---- NLM Model Specific Arguments ----
    NLMWrapperActor.add_model_specific_args(parser)

    # ---- Critic loss weight ----
    parser.add_argument(
        '--critic-loss-weight', type=float, default=0.1,
        help="Weight for critic loss vs actor loss"
    )

    # ---- PPO policy-specific arguments ----
    PPOSolverPolicy.add_model_specific_args(parser)

    args = parser.parse_args()
    return args


def validate_args(args):
    """Validate arguments."""
    if args.steps_per_level < 1:
        raise ValueError("--steps-per-level must be > 0")
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
    if args.disc_factor < 0 or args.disc_factor > 1:
        raise ValueError("--disc-factor must be in [0, 1]")
    if args.gae_factor < 0 or args.gae_factor > 1:
        raise ValueError("--gae-factor must be in [0, 1]")

    # Convert to absolute paths
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

    # Compute test difficulty defaults (hardest level)
    if args.test_min_blocks is None:
        args.test_min_blocks = args.min_blocks_start + (args.max_levels - 1) * args.blocks_increment
    if args.test_max_blocks is None:
        args.test_max_blocks = args.max_blocks_start + (args.max_levels - 1) * args.blocks_increment

    return args


# =====================================================================
# Curriculum Level Helper
# =====================================================================

def get_level_blocks(args, level: int) -> Tuple[int, int]:
    """
    Get min/max blocks for a given curriculum level.
    
    Level 1: (min_blocks_start, max_blocks_start)
    Level 2: (min_blocks_start + increment, max_blocks_start + increment)
    ...
    """
    min_blocks = args.min_blocks_start + (level - 1) * args.blocks_increment
    max_blocks = args.max_blocks_start + (level - 1) * args.blocks_increment
    return min_blocks, max_blocks


# =====================================================================
# Problem Generation
# =====================================================================

def generate_problems(generator_path: str, out_dir: str,
                      count: int, min_blocks: int, max_blocks: int,
                      seed_start: int = 0) -> None:
    """
    Generate PDDL problems using the blocksworld generator binary.
    
    Parameters
    ----------
    generator_path : str
        Path to the blocksworld generator binary
    out_dir : str
        Output directory for generated .pddl files
    count : int
        Number of problems to generate
    min_blocks : int
        Minimum number of blocks
    max_blocks : int
        Maximum number of blocks
    seed_start : int
        Starting seed for generation
    """
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    # Remove existing problems
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
# Problem Loading
# =====================================================================

def load_problems_from_dir(problem_dir: str, domain_path: str,
                           num_problems: int, max_actions=None) -> List[PDDLProblem]:
    """Load problems from directory with fresh parser for each problem."""
    problem_dir = Path(problem_dir)
    problem_files = sorted(problem_dir.glob("*.pddl"))

    if not problem_files:
        raise FileNotFoundError(f"No .pddl files in {problem_dir}")

    problems = []
    for i in range(num_problems):
        problem_file = problem_files[i % len(problem_files)]
        fresh_parser = Parser()
        fresh_parser.parse_domain(str(domain_path))

        problem = PDDLProblem.load_from_pddl(fresh_parser, str(problem_file))
        if problem is not None:
            if max_actions is not None:
                if isinstance(max_actions, tuple):
                    problem.max_actions = max_actions[i % len(max_actions)]
                else:
                    problem.max_actions = max_actions
            problems.append(problem)

    return problems


# =====================================================================
# Experiment Management
# =====================================================================

def get_experiment_id(args) -> str:
    """Generate unique experiment ID from arguments."""
    included_args = {k: v for k, v in vars(args).items() if k not in EXCLUDED_ARGS_ID}
    full_hash = hashlib.sha256(str(included_args).encode()).hexdigest()[:ID_LENGTH]
    return full_hash


def save_experiment_info(filepath, args, experiment_id: str,
                         best_train_it: int, last_train_it: int,
                         best_val_score: float, curr_level: int) -> None:
    """Save experiment metadata to JSON."""
    experiment_info = {k: v for k, v in vars(args).items() if k not in EXCLUDED_ARGS_ID}
    experiment_info['experiment_id'] = experiment_id
    experiment_info['best_train_it'] = best_train_it
    experiment_info['last_train_it'] = last_train_it
    experiment_info['best_val_score'] = best_val_score
    experiment_info['curr_level'] = curr_level
    experiment_info.update(ADDITIONAL_EXPERIMENT_INFO)

    with open(filepath, 'w') as f:
        json.dump(experiment_info, f, indent=2)


def read_experiment_info(experiment_info_path: Path):
    """Read previous experiment metadata."""
    if experiment_info_path.exists():
        with open(experiment_info_path, 'r') as f:
            info = json.load(f)
            return (
                info.get('best_train_it', 0),
                info.get('last_train_it', 0),
                info.get('best_val_score', -1),
                info.get('curr_level', 1),
            )
    return 0, 0, -1, 1


# =====================================================================
# Policy Creation
# =====================================================================

def create_policy(args, parser, last_train_it: int,
                  experiment_folder_path: Path, device: torch.device) -> GenerativePolicy:
    """Create or load policy."""
    if args.policy_type == 'random':
        return RandomPolicy()

    domain_actions = set([
        (action[0], tuple([var for var, var_class in zip(action[1][0], action[1][1])
                           if var_class == 'param']))
        for action in parser.actions
    ])

    dummy_state = PDDLState(
        types=parser.types,
        type_hierarchy=parser.type_hierarchy,
        predicates=domain_actions,
        objects=[],
        atoms=set()
    )

    args_dict = vars(args)
    actor_args = {'dummy_pddl_state': dummy_state}
    critic_args = {'dummy_pddl_state': dummy_state}

    if args.train_mode == "supersede" or last_train_it == 0:
        policy = PPOSolverPolicy(
            args=args_dict,
            actor_class=NLMWrapperActor,
            actor_arguments=actor_args,
            critic_class=NLMWrapperCritic,
            critic_arguments=critic_args,
            device=device
        )
    elif args.train_mode == "resume":
        ckpt_path = experiment_folder_path / CKPTS_FOLDER_NAME / 'last.ckpt'
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


# =====================================================================
# Curriculum Training Loop
# =====================================================================

def evaluate_val_success_rate(trainer: PolicyTrainer, val_dir: str,
                              args) -> float:
    """
    Evaluate success rate on val problems.
    Used to decide whether to advance to the next level.
    """
    val_problems = load_problems_from_dir(
        val_dir, args.domain_path,
        args.num_problems_val,
        max_actions=args.max_actions_val
    )

    with torch.no_grad():
        is_solved, val_info, val_trajectories, _ = trainer._solve_and_collect_trajectories(
            val_problems, args.max_actions_val
        )

    success_count = sum(1 for p in val_info if p.get('goal_reached', False))
    success_rate = success_count / len(val_info) if val_info else 0.0
    return success_rate


def train_curriculum(args, parser, experiment_id: str,
                     experiment_folder_path: Path) -> None:
    """
    Main curriculum training loop.
    
    Trains the same policy across all levels, advancing when the agent
    achieves >= advance_threshold success rate on val problems.
    """
    experiment_info_path = experiment_folder_path / EXPERIMENT_INFO_FILENAME
    experiment_folder_path.mkdir(parents=True, exist_ok=True)

    # Read previous progress
    best_train_it, last_train_it, best_val_score, start_level = read_experiment_info(
        experiment_info_path
    )

    print(f"Previous progress: best={best_train_it}, last={last_train_it}, "
          f"score={best_val_score:.3f}, level={start_level}")

    # Reset if superseding
    if args.train_mode == "supersede" or last_train_it == 0:
        remove_if_exists(experiment_folder_path / LOGS_FOLDER_NAME)
        remove_if_exists(experiment_folder_path / CKPTS_FOLDER_NAME)
        remove_if_exists(experiment_folder_path / VAL_FOLDER_NAME)
        remove_if_exists(experiment_folder_path / TEST_FOLDER_NAME)
        best_train_it = 0
        last_train_it = 0
        best_val_score = -1
        start_level = 1

    if args.train_mode == 'skip' or args.policy_type == 'random':
        return

    # Create policy (shared across all levels)
    device = torch.device("cuda" if args.device == 'gpu' else "cpu")
    policy = create_policy(args, parser, last_train_it, experiment_folder_path, device)

    # Global iteration counter (across all levels, used for TensorBoard x-axis)
    global_it = last_train_it

    # ---- Curriculum Loop ----
    for level in range(start_level, args.max_levels + 1):
        min_blocks, max_blocks = get_level_blocks(args, level)

        print(f"\n{'='*70}")
        print(f"CURRICULUM LEVEL {level}/{args.max_levels} "
              f"({min_blocks}-{max_blocks} blocks)")
        print(f"{'='*70}\n")

        # Directories for this level's problems
        level_train_dir = Path(args.data_dir) / f"level_{level}" / "train"
        level_val_dir   = Path(args.data_dir) / f"level_{level}" / "val"

        # Generate train+val problems for this level
        print(f"  Generating problems for level {level}...")
        seed_offset = level * 10000  # Different seeds per level
        generate_problems(
            args.generator_path, str(level_train_dir),
            args.num_problems_train, min_blocks, max_blocks,
            seed_start=seed_offset
        )
        generate_problems(
            args.generator_path, str(level_val_dir),
            args.num_problems_val, min_blocks, max_blocks,
            seed_start=seed_offset + args.num_problems_train
        )

        # Create problem solver and trainer for this level
        # (same policy, new solver/trainer to allow fresh logging context)
        problem_solver = ProblemSolver(
            parser, policy,
            reward_goal_reached=args.reward_goal_reached,
            reward_step=args.reward_step,
            reward_efficiency=args.reward_efficiency
        )
        trainer = PolicyTrainer(
            args, experiment_folder_path, problem_solver, policy, device
        )

        # Define problem loading functions for this level
        def get_train_problems():
            return load_problems_from_dir(
                str(level_train_dir), args.domain_path,
                args.num_problems_train, max_actions=args.max_actions_train
            )

        def get_val_problems():
            return load_problems_from_dir(
                str(level_val_dir), args.domain_path,
                args.num_problems_val, max_actions=args.max_actions_val
            )

        # ---- Level Training Loop ----
        level_it = 0
        advanced = False

        if device.type == 'cuda':
            policy.to('cuda')

        while level_it < args.steps_per_level:
            global_it += 1
            level_it += 1
            best_val_score = -1

            print(f"\n  [Level {level}] Iteration {level_it}/{args.steps_per_level} "
                  f"(global: {global_it})")

            # Collect trajectories
            with torch.no_grad():
                train_problems = get_train_problems()
                is_solved, problem_info, trajectories, elapsed = \
                    trainer._solve_and_collect_trajectories(
                        train_problems, args.max_actions_train
                    )

            if len(trajectories) == 0:
                print("    No trajectories collected, skipping")
                continue

            # Process and train
            samples = trainer._process_trajectories(trajectories, problem_info)
            trainer._perform_train_step(samples)

            # Save last checkpoint
            trainer.save_policy(save_best=False)

            # Logging
            with torch.no_grad():
                if global_it % args.log_period == 0:
                    trainer.log_metrics('train', global_it, problem_info,
                                       trajectories=trajectories)

                # Check advancement condition
                if level_it % args.check_advance_period == 0:
                    val_success_rate = evaluate_val_success_rate(
                        trainer, str(level_val_dir), args
                    )
                    print(f"    Val success rate: {val_success_rate:.1%} "
                          f"(threshold: {args.advance_threshold:.1%})")

                    # Log val metrics
                    val_problems_eval = load_problems_from_dir(
                        str(level_val_dir), args.domain_path,
                        args.num_problems_val, max_actions=args.max_actions_val
                    )
                    _, val_info, _, _ = trainer._solve_and_collect_trajectories(
                        val_problems_eval, args.max_actions_val
                    )

                    successful = [p for p in val_info if p.get('goal_reached', False)]
                    mean_eff = (sum(p['efficiency'] for p in successful) / len(successful)
                               if successful else 0.0)
                    val_score = val_success_rate * mean_eff

                    trainer.log_metrics('val', global_it, val_info, score=val_score)

                    # Save best checkpoint
                    if val_score > best_val_score:
                        best_val_score = val_score
                        best_train_it = global_it
                        trainer.save_policy(save_best=True)
                        print(f"    ✓ New best score: {val_score:.3f}")

                    # Advance to next level?
                    if val_success_rate >= args.advance_threshold:
                        print(f"\n  ✓ Level {level} complete! "
                              f"Val success rate {val_success_rate:.1%} >= "
                              f"{args.advance_threshold:.1%}")
                        advanced = True
                        break

            # Update logging iteration
            policy.curr_logging_it += 1

            # Save experiment progress
            save_experiment_info(
                experiment_info_path, args, experiment_id,
                best_train_it, global_it, best_val_score, level
            )

        if not advanced:
            print(f"\n  Max steps ({args.steps_per_level}) reached at level {level}, "
                  f"advancing anyway")

        trainer.close_writers()

    # Save final progress
    save_experiment_info(
        experiment_info_path, args, experiment_id,
        best_train_it, global_it, best_val_score, args.max_levels
    )

    print(f"\n{'='*70}")
    print(f"Curriculum Training Complete!")
    print(f"  Best iteration: {best_train_it}")
    print(f"  Last iteration: {global_it}")
    print(f"  Best val score: {best_val_score:.3f}")
    print(f"{'='*70}\n")


# =====================================================================
# Testing
# =====================================================================

def test(args, parser, experiment_id: str, experiment_folder_path: Path) -> None:
    """
    Test the trained policy on fixed hard problems.
    Test problems are generated once at the hardest difficulty level.
    """
    if args.test_mode == 'skip':
        return

    experiment_info_path = experiment_folder_path / EXPERIMENT_INFO_FILENAME
    test_folder_path = experiment_folder_path / TEST_FOLDER_NAME

    # Check if we have a trained policy
    if args.policy_type != 'random':
        ckpt_path = experiment_folder_path / CKPTS_FOLDER_NAME / 'best.ckpt'
        if not ckpt_path.exists():
            print("Skipping test: no trained policy found")
            return

    # Reset test if superseding
    if args.test_mode == 'supersede':
        remove_if_exists(test_folder_path)

    test_folder_path.mkdir(parents=True, exist_ok=True)

    # Generate fixed test problems (hardest difficulty)
    test_problems_dir = Path(args.data_dir) / "test"
    print(f"\n  Generating test problems "
          f"({args.test_min_blocks}-{args.test_max_blocks} blocks)...")
    generate_problems(
        args.generator_path, str(test_problems_dir),
        args.num_problems_test,
        args.test_min_blocks, args.test_max_blocks,
        seed_start=999000  # Fixed seed for reproducibility
    )

    # Load policy
    device = torch.device("cuda" if args.device == 'gpu' else "cpu")

    if args.policy_type == 'random':
        policy = RandomPolicy()
    else:
        domain_actions = set([
            (action[0], tuple([var for var, var_class in zip(action[1][0], action[1][1])
                               if var_class == 'param']))
            for action in parser.actions
        ])
        dummy_state = PDDLState(
            types=parser.types,
            type_hierarchy=parser.type_hierarchy,
            predicates=domain_actions,
            objects=[],
            atoms=set()
        )
        args_dict = vars(args)
        actor_args = {'dummy_pddl_state': dummy_state}
        critic_args = {'dummy_pddl_state': dummy_state}

        ckpt_path = experiment_folder_path / CKPTS_FOLDER_NAME / 'best.ckpt'
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

    # Move to device
    if device.type == 'cuda':
        policy.to('cuda')

    # Create solver and trainer
    problem_solver = ProblemSolver(
        parser, policy,
        reward_goal_reached=args.reward_goal_reached,
        reward_step=args.reward_step,
        reward_efficiency=args.reward_efficiency
    )
    trainer = PolicyTrainer(args, experiment_folder_path, problem_solver, policy, device)

    def get_test_problems():
        return load_problems_from_dir(
            str(test_problems_dir), args.domain_path,
            args.num_problems_test, max_actions=args.max_actions_test
        )

    trainer.test(test_problems_fn=get_test_problems)


# =====================================================================
# Main
# =====================================================================

def main(args):
    """Main entry point."""
    os.chdir(dirname(dirname(dirname(dirname(abspath(__file__))))))

    seed_everything(args.seed, workers=True)

    experiment_id = get_experiment_id(args)
    print(f"\n>>> Experiment ID: {experiment_id}\n")

    experiments_dir = Path(args.experiments_dir)
    experiment_folder_path = experiments_dir / experiment_id

    # Parse domain
    parser = Parser()
    parser.parse_domain(args.domain_path)

    # Curriculum training
    train_curriculum(args, parser, experiment_id, experiment_folder_path)

    # Test on fixed hard problems
    test(args, parser, experiment_id, experiment_folder_path)

    print("\n>>> Done!")
    print(f">>> Experiment ID: {experiment_id}\n")


if __name__ == '__main__':
    args = parse_arguments()
    args = validate_args(args)
    main(args)