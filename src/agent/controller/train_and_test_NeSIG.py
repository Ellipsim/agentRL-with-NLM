"""
> train_and_test_NeSIG.py

Training script for the NeSIG teacher + student co-training baseline.

The training loop alternates between:
  1. NeSIG (teacher) generates N problems
  2. Student attempts to solve each problem → trajectories
  3. Student PPO update  (every iteration)
  4. Difficulty reward calculated from updated student performance
  5. NeSIG PPO update   (every --teacher-update-period iterations)
  6. Every --test-period steps: evaluate student on fixed test set

Usage:
    python -m src.agent.controller.train_and_test_NeSIG \
        --domain-path data/domains/blocksworld.pddl \
        --device gpu \
        --seed 1 \
        --steps 200 \
        --num-problems-train 20 \
        --num-problems-test 100 \
        --test-period 20 \
        --teacher-update-period 1 \
        --max-init-actions-train 10 \
        --max-goal-actions-train 10 \
        --train-mode supersede \
        --test-mode supersede
"""

import argparse
import hashlib
import json
import os
import sys
import random
import shutil
import torch
from copy import deepcopy
from pathlib import Path
from os.path import dirname, abspath
from typing import List, Optional, Tuple
from pytorch_lightning import seed_everything
from lifted_pddl import Parser

# ---- NeSIG imports ----
from src.nesig.constants import DOMAIN_INFO, TRAIN_PLANNER_ARGS
from src.nesig.learning.generative_policy import PPOPolicy, RandomPolicy
from src.nesig.learning.model_wrapper import NLMWrapper, NLMWrapperActor, NLMWrapperCritic
from src.nesig.symbolic.pddl_state import PDDLState as NeSIGPDDLState
from src.nesig.symbolic.problem_generator import ProblemGenerator
from src.nesig.metrics.consistency_evaluators.dummy_consistency import DummyConsistencyEvaluator
from src.nesig.metrics.diversity import InitGoalDiversityEvaluator
from src.nesig.controller.trainer import PolicyTrainer as NeSIGTrainer

_nesig_teacher_root = Path(__file__).resolve().parents[3] / 'nesig_teacher'
for domain_key in DOMAIN_INFO:
    for field in ('path',):
        if field in DOMAIN_INFO[domain_key]:
            DOMAIN_INFO[domain_key][field] = _nesig_teacher_root / DOMAIN_INFO[domain_key][field]

from src.nesig import constants as nesig_constants
nesig_constants.PLANNER_SCRIPTS_PATH = _nesig_teacher_root / 'src/nesig/libs/planner-scripts'


# ---- Student imports ----
from src.agent.constants import (
    EXPERIMENT_INFO_FILENAME, LOGS_FOLDER_NAME, CKPTS_FOLDER_NAME,
    TEST_FOLDER_NAME, remove_if_exists, EXCLUDED_ARGS_ID, ID_LENGTH,
    ADDITIONAL_EXPERIMENT_INFO,
)
from src.agent.learning.generative_policy import PPOSolverPolicy
from src.agent.learning.model_wrapper import (
    NLMWrapperActor as StudentNLMWrapperActor,
    NLMWrapperCritic as StudentNLMWrapperCritic,
)
from src.agent.pddl.problem_solver import ProblemSolver
from src.agent.pddl.pddl_state import PDDLState as StudentPDDLState
from src.agent.controller.trainer import PolicyTrainer as StudentTrainer, ReplayBuffer, REPLAY_BUFFER_FILENAME

# TODO: Copiar todas estas funciones
from src.agent.controller.train_and_test_ACG import (
    load_problems_from_dir, generate_problems, get_level_blocks,
    save_experiment_info, read_last_train_it, create_policy,
    save_level_checkpoint,
)
from src.agent.teacher.student_difficulty_evaluator import StudentDifficultyEvaluator


# =====================================================================
# Argument Parsing
# =====================================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Co-train NeSIG teacher + student solver.",
    )

    # ---- Domain ----
    parser.add_argument('--domain-path', type=str, required=True,
                        help="Path to the shared domain PDDL file")
    parser.add_argument('--nesig-domain', type=str, default='blocksworld',
                        choices=tuple(DOMAIN_INFO.keys()),
                        help="NeSIG domain name (must match domain-path)")
    
    # ---- Test problems evaluation ----
    parser.add_argument('--test-problems-dir', type=str, default='./data/problems/test',
                            help="Directory with test problems. Used as-is unless "
                                "--generate-test-problems is set.")
    parser.add_argument('--generate-test-problems', action='store_true',
                            help="Generate test problems using the binary generator into "
                                "--test-problems-dir instead of using existing ones.")
    parser.add_argument('--test-min-blocks', type=int, default=2)
    parser.add_argument('--test-max-blocks', type=int, default=30)
    parser.add_argument('--generator-path', type=str, default='./problem_generator/pddl-generators/blocksworld/blocksworld')
    parser.add_argument('--test-period', type=int, default=20,
                            help="Steps between student test evaluations")
    parser.add_argument('--num-problems-test', type=int, default=300)
    parser.add_argument('--max-actions-test', type=int, default=None)
    parser.add_argument('--data-dir', type=str, default='./data/problems/nesig')


    # ---- NeSIG teacher ----
    parser.add_argument('--max-init-actions-train', type=int, default=10,
                        help="Max init actions for NeSIG problem generation (controls problem size)")
    parser.add_argument('--max-goal-actions-train', type=int, default=10,
                            help="Max goal actions for NeSIG problem generation")
    parser.add_argument('--nesig-ppo-epochs', type=int, default=3,
                            help="PPO epochs for teacher update")
    parser.add_argument('--nesig-lr', type=float, default=1e-3,
                            help="Learning rate for teacher")
    parser.add_argument('--diversity-threshold', type=float, default=0.25)
    parser.add_argument('--perc-problems-diversity', type=float, default=1.0)
    parser.add_argument('--r-eventual-consistency', type=float, default=-1.0)
    parser.add_argument('--consistency-evaluator', choices=('dummy', 'domain'), default='domain')
    parser.add_argument('--policy-type', choices=('random', 'PPO'), default='PPO')
    
    
    # ---- Student ----
    parser.add_argument('--reward-goal-reached', type=float, default=1.0)
    parser.add_argument('--reward-step', type=float, default=-1)
    parser.add_argument('--max-actions-train', type=int, default=None,
                        help="Action budget for student during training "
                             "(defaults to max-actions-test if not set)")

    # ---- Shared training ----    
    parser.add_argument('--steps', type=int, default=200,
                            help="Total co-training iterations")
    parser.add_argument('--teacher-update-period', type=int, default=1,
                            help="Update teacher every N student iterations")
    parser.add_argument('--difficulty-penalty', type=float, default=0.0,
                            help="Difficulty reward given to NeSIG when student fails")
    parser.add_argument('--num-problems-train', type=int, default=20,
                            help="Problems generated per iteration")
    parser.add_argument('--nesig-warmup-steps', type=int, default=30,
                            help="NeSIG-only warmup steps before co-training. Set 0 to disable.")
    parser.add_argument('--min-samples-train', type=int, default=10)
    parser.add_argument('--problem-generation-period', type=int, default=None,
                    help="Generate new problems every N steps. "
                         "Defaults to --teacher-update-period if not set.")

    
    parser.add_argument('--batch-size', type=int, default=64)
    parser.add_argument('--grad-clip', type=float, default=0.5)
    parser.add_argument('--disc-factor', type=float, default=0.99)
    parser.add_argument('--gae-factor', type=float, default=0.95)

    # --- Training Set Up ---
    parser.add_argument('--seed', type=int, default=1)
    parser.add_argument('--run-id', type=int, default=0)
    parser.add_argument('--device', type=str, choices=('gpu', 'cpu'), default='gpu')
    

    # ---- Training problem accumulation ----
    parser.add_argument('--max-generation-attempts', type=int, default=30,
                        help="Max NeSIG generation batches per step before giving up")

    # ---- Experience replay ----
    parser.add_argument('--replay-extra', type=int, default=0,
                    help="Number of extra problems to add from replay buffer "
                         "on top of the NeSIG generated ones. Set 0 to disable.")
    parser.add_argument('--replay-buffer-size', type=int, default=3000)

    # ---- Logging ----
    parser.add_argument('--log-period', type=int, default=1)
    parser.add_argument('--save-level-checkpoints', action='store_true')

    # ---- Modes ----
    parser.add_argument('--train-mode', choices=('skip', 'supersede', 'resume'),
                        default='resume')
    parser.add_argument('--test-mode', choices=('skip', 'supersede', 'missing'),
                        default='missing')
    parser.add_argument('--experiments-dir', type=str, default='./experiments')

    # ---- NLM model args ----
    StudentNLMWrapperActor.add_model_specific_args(parser)
    parser.add_argument('--critic-loss-weight', type=float, default=0.1)
    PPOSolverPolicy.add_model_specific_args(parser)

    return parser.parse_args()


def validate_args(args):
    if args.steps < 1:
        raise ValueError("--steps must be > 0")
    if args.grad_clip == -1:
        args.grad_clip = None
    elif args.grad_clip <= 0:
        raise ValueError("--grad-clip must be > 0 or -1")
    if args.max_actions_test is None:
        args.max_actions_test = 4 * (args.test_max_blocks - 1)
    if args.max_actions_train is None:
        args.max_actions_train = args.max_actions_test
    args.domain_path = str(Path(args.domain_path).resolve())
    if not Path(args.domain_path).exists():
        raise ValueError(f"Domain file not found: {args.domain_path}")
    if args.problem_generation_period is None:
        args.problem_generation_period = args.teacher_update_period
    args.policy_type = 'PPO'
    return args


# =====================================================================
# Experiment Management
# =====================================================================

def get_experiment_id(args):
    included = {k: v for k, v in vars(args).items() if k not in EXCLUDED_ARGS_ID}
    return hashlib.sha256(str(included).encode()).hexdigest()[:ID_LENGTH]


# =====================================================================
# NeSIG Setup
# =====================================================================

def build_nesig_components(args, device):
    """
    Build NeSIG's parsed domain info, init/goal policies, and problem generator.
    The difficulty evaluator is set to None here — it is injected after the
    student is built, since it depends on the student solver.
    """
    import argparse
    from src.nesig.controller.train_and_test import parse_domain_and_obtain_info

    # Build a Namespace for NeSIG (PyTorch Lightning requires argparse.Namespace)
    nesig_args = argparse.Namespace(
        domain=args.nesig_domain,
        consistency_evaluator=args.consistency_evaluator,
        r_eventual_consistency=args.r_eventual_consistency,
        diversity_threshold=args.diversity_threshold,
        perc_problems_diversity=args.perc_problems_diversity,
        max_init_actions_train=args.max_init_actions_train,
        max_goal_actions_train=args.max_goal_actions_train,
        max_init_actions_val=args.max_init_actions_train,
        max_goal_actions_val=args.max_goal_actions_train,
        num_problems_train=args.num_problems_train,
        num_problems_val=args.num_problems_train,
        num_problems_test=args.num_problems_test,
        min_samples_train=args.min_samples_train,
        critic_loss_weight=args.critic_loss_weight,
        grad_clip=args.grad_clip,
        batch_size=args.batch_size,
        disc_factor=1.0,
        gae_factor=1.0,
        weight_decay=0.0,
        init_policy='PPO',
        goal_policy='PPO',
        ML_model='NLM',
        # ---- init phase PPO args ----
        init_term_action_prob=0.0,
        init_lr=args.nesig_lr,
        init_PPO_epochs=args.nesig_ppo_epochs,
        init_epsilon=0.2,
        init_entropy_coeffs=0.0,
        init_lifted_entropy_weight=0.5,
        # ---- goal phase PPO args ----
        goal_term_action_prob=0.0,
        goal_lr=args.nesig_lr,
        goal_PPO_epochs=args.nesig_ppo_epochs,
        goal_epsilon=0.2,
        goal_entropy_coeffs=0.0,
        goal_lifted_entropy_weight=0.5,
    )

    # Forward all remaining args from student (NLM-specific, PPO-specific, etc.)
    for attr, value in vars(args).items():
        if not hasattr(nesig_args, attr):
            setattr(nesig_args, attr, value)

    parsed_domain_info = parse_domain_and_obtain_info(nesig_args)

    # Build NeSIG init and goal policies
    actor_class = NLMWrapperActor
    critic_class = NLMWrapperCritic

    init_actor_args = {'dummy_pddl_state': parsed_domain_info['dummy_state_init']}
    goal_actor_args = {'dummy_pddl_state': parsed_domain_info['dummy_state_goal']}

    init_policy = PPOPolicy(
        phase='init', args=nesig_args,
        actor_class=actor_class, actor_arguments=init_actor_args,
        critic_class=critic_class, critic_arguments=deepcopy(init_actor_args),
        device=device,
    )
    goal_policy = PPOPolicy(
        phase='goal', args=nesig_args,
        actor_class=actor_class, actor_arguments=goal_actor_args,
        critic_class=critic_class, critic_arguments=deepcopy(goal_actor_args),
        device=device,
    )

    diversity_evaluator = InitGoalDiversityEvaluator(
        r_diversity_weight=1.0,
        perc_problems_diversity=args.perc_problems_diversity,
    )

    # Problem generator without difficulty evaluator — injected later
    problem_generator = ProblemGenerator(
        parsed_domain_info['parser'],
        init_policy, goal_policy,
        parsed_domain_info['consistency_evaluator'],
        parsed_domain_info['goal_predicates'],
        parsed_domain_info['init_state_info'],
        parsed_domain_info['allowed_virtual_objects'],
        difficulty_evaluator=None,
        diversity_evaluator=diversity_evaluator,
    )

    if device.type == 'cuda':
        init_policy.to('cuda')
        goal_policy.to('cuda')

    return nesig_args, parsed_domain_info, init_policy, goal_policy, problem_generator


# =====================================================================
# Student Setup
# =====================================================================

def build_student(args, domain_parser, last_train_it, experiment_folder_path, device):
    """Build the student policy and problem solver."""

    student_policy = create_policy(args, domain_parser, last_train_it, experiment_folder_path, device)

    student_solver = ProblemSolver(
        domain_parser, student_policy,
        reward_goal_reached=args.reward_goal_reached,
        reward_step=args.reward_step
    )

    return student_policy, student_solver

# =====================================================================
# Metrics logger for shared training
# =====================================================================

def log_nesig_student_metrics(
    student_trainer: StudentTrainer,
    consistent_problems: list,
    last_problem_info: list,
    new_difficulty_rewards: list,
    current_step: int,
) -> None:
    """Log NeSIG-student interaction metrics to TensorBoard and stdout."""

    # ---- Problem size metrics ----
    # NeSIG problems don't directly expose num_blocks, but we can infer
    # from the number of objects in the problem info after student solves them
    num_objects_list = [
        info.get('num_objects', {})
        for info in last_problem_info
        if info.get('consistency', False)
    ]
    # Count total objects as proxy for problem size
    problem_sizes = [sum(v for v in obj.values()) for obj in num_objects_list if obj]
    mean_size = sum(problem_sizes) / len(problem_sizes) if problem_sizes else 0.0

    # ---- Difficulty metrics ----
    num_solved_by_student = sum(1 for d in new_difficulty_rewards if d > 0)
    fraction_solved = num_solved_by_student / len(new_difficulty_rewards) if new_difficulty_rewards else 0.0
    mean_difficulty = sum(new_difficulty_rewards) / len(new_difficulty_rewards) if new_difficulty_rewards else 0.0

    # ---- Consistency rate from last batch ----
    consistency_rate = sum(
        1 for info in last_problem_info if info.get('consistency', False)
    ) / len(last_problem_info) if last_problem_info else 0.0

    # ---- Print summary ----
    print(f"  \033[1m\033[96m[NESIG-STUDENT METRICS]\033[0m")
    print(f"    Consistency rate    : {consistency_rate:.1%} "
          f"({sum(1 for i in last_problem_info if i.get('consistency', False))}"
          f"/{len(last_problem_info)} consistent)")
    print(f"    Student solved      : {num_solved_by_student}/{len(new_difficulty_rewards)} "
          f"({fraction_solved:.1%})")
    print(f"    Mean difficulty     : {mean_difficulty:.3f}  "
          f"(0=trivial, 1=hard, 0=failed)")
    if problem_sizes:
        print(f"    Mean problem size   : {mean_size:.1f} objects")

    # ---- Log to TensorBoard ----
    writer = student_trainer.writers['train']
    writer.add_scalar('NeSIG/consistency_rate', consistency_rate, global_step=current_step)
    writer.add_scalar('NeSIG/fraction_solved_by_student', fraction_solved, global_step=current_step)
    writer.add_scalar('NeSIG/mean_difficulty_reward', mean_difficulty, global_step=current_step)
    writer.add_scalar('NeSIG/num_consistent_problems', len(consistent_problems), global_step=current_step)
    if problem_sizes:
        writer.add_scalar('NeSIG/mean_problem_size', mean_size, global_step=current_step)

# =====================================================================
# Generator problem helper
# =====================================================================

def accumulate_consistent_problems(
    nesig_trainer,
    target: int,
    init_actions: int,
    goal_actions: int,
    max_attempts: int,
) -> Tuple[list, list, list]:
    """
    Keep asking NeSIG to generate problems until we have `target` consistent
    ones or `max_attempts` batches have been generated, whichever comes first.

    Returns
    -------
    consistent_problems : List[NeSIGProblem]
        Consistent problems trimmed to target.
    consistent_infos : List[Dict]
        Info dicts for each consistent problem.
    consistent_trajectories : List
        Trajectories for each consistent problem.
    """
    consistent_problems = []
    consistent_infos = []
    consistent_trajectories = []
    attempts = 0

    while len(consistent_problems) < target and attempts < max_attempts:
        with torch.no_grad():
            problems, problem_info_list, trajectories, _, _ = \
                nesig_trainer._generate_problems_and_trajectories(
                    target,
                    init_actions,
                    goal_actions,
                )

        new_consistent = [
            (p, info, traj)
            for p, info, traj in zip(problems, problem_info_list, trajectories)
            if info['consistency']
        ]

        consistent_problems.extend(p for p, _, _ in new_consistent)
        consistent_infos.extend(info for _, info, _ in new_consistent)
        consistent_trajectories.extend(traj for _, _, traj in new_consistent)

        attempts += 1

        if not new_consistent:
            print(f"    [generation] attempt {attempts}/{max_attempts}: "
                  f"0 consistent problems")
        else:
            print(f"    [generation] attempt {attempts}/{max_attempts}: "
                  f"{len(new_consistent)} consistent, "
                  f"total={len(consistent_problems)}/{target}")

    if len(consistent_problems) < target:
        print(f"  Warning: only {len(consistent_problems)}/{target} consistent "
              f"problems after {max_attempts} attempts")
    elif len(consistent_problems) > target:
        print(f"  Trimming {len(consistent_problems)} → {target} problems")
        consistent_problems = consistent_problems[:target]
        consistent_infos = consistent_infos[:target]
        consistent_trajectories = consistent_trajectories[:target]

    return consistent_problems, consistent_infos, consistent_trajectories

# =====================================================================
# Checkpoint helper
# =====================================================================

def save_policy_checkpoint(policy_obj, ckpt_path: Path) -> None:
    """Save policy checkpoint safely, removing problematic sharded tensor hooks."""
    hooks_to_restore = []
    for module in policy_obj.modules():
        bad_hooks = [h for h in module._state_dict_hooks.values()
                     if 'sharded_tensor' in getattr(h, '__module__', '')]
        for hook in bad_hooks:
            handle = next(k for k, v in module._state_dict_hooks.items() if v is hook)
            hooks_to_restore.append((module, handle, hook))
            del module._state_dict_hooks[handle]

    try:
        state_dict = {k: v.cpu().clone() for k, v in policy_obj.state_dict().items()}
        ckpt_path.parent.mkdir(parents=True, exist_ok=True)
        torch.save({'state_dict': state_dict}, str(ckpt_path))
    finally:
        for module, handle, hook in hooks_to_restore:
            module._state_dict_hooks[handle] = hook

# =====================================================================
# Main Training Loop
# =====================================================================

def train(args, experiment_id, experiment_folder_path: Path):
    experiment_info_path = experiment_folder_path / EXPERIMENT_INFO_FILENAME
    experiment_folder_path.mkdir(parents=True, exist_ok=True)

    last_train_it = read_last_train_it(experiment_info_path)
    print(f"Previous progress: last_train_it={last_train_it}")

    if args.train_mode == 'supersede':
        for folder in (LOGS_FOLDER_NAME, CKPTS_FOLDER_NAME, TEST_FOLDER_NAME):
            remove_if_exists(experiment_folder_path / folder)
        p = experiment_folder_path / REPLAY_BUFFER_FILENAME
        if p.exists():
            p.unlink()
        last_train_it = 0
        data_dir = Path(args.data_dir)
        if data_dir.exists():
            shutil.rmtree(data_dir)
            data_dir.mkdir(parents=True, exist_ok=True)

    save_experiment_info(experiment_info_path, args, experiment_id, last_train_it)

    if args.train_mode == 'skip':
        return

    device = torch.device('cuda' if args.device == 'gpu' else 'cpu')

    # ---- Build student ----
    domain_parser = Parser()
    domain_parser.parse_domain(args.domain_path)

    student_policy, student_solver = build_student(
        args, domain_parser, last_train_it, experiment_folder_path, device
    )

    if device.type == 'cuda':
        student_policy.to('cuda')

    # ---- Build NeSIG teacher ----
    nesig_args, parsed_domain_info, init_policy, goal_policy, problem_generator = \
        build_nesig_components(args, device)

    # Move NeSIG policies to device
    if device.type == 'cuda':
        init_policy.to('cuda')
        goal_policy.to('cuda')

    # ---- Student performance evaluator for NeSIG reward ----
    difficulty_evaluator = StudentDifficultyEvaluator(
        max_actions=args.max_actions_train,
        penalty=args.difficulty_penalty,
    )

    # ---- Build trainers ----
    student_trainer = StudentTrainer(
        args, experiment_folder_path, student_solver, student_policy, device
    )
    nesig_trainer = NeSIGTrainer(
        nesig_args, experiment_folder_path / 'nesig',
        problem_generator, init_policy, goal_policy, device=device,
    )

    # ---- Load NeSIG checkpoints on resume ----
    if args.train_mode == 'resume' and last_train_it > 0:
        nesig_ckpt_dir = experiment_folder_path / 'nesig' / 'checkpoints'
        init_ckpt = nesig_ckpt_dir / 'init_last.ckpt'
        goal_ckpt = nesig_ckpt_dir / 'goal_last.ckpt'
        if init_ckpt.exists() and goal_ckpt.exists():
            print(f"  Loading NeSIG checkpoints from {nesig_ckpt_dir}")
            init_policy.load_state_dict(torch.load(str(init_ckpt), map_location=device)['state_dict'])
            goal_policy.load_state_dict(torch.load(str(goal_ckpt), map_location=device)['state_dict'])
        else:
            print(f"  Warning: NeSIG checkpoints not found, starting from scratch")

    # ---- NeSIG warmup ----
    if last_train_it == 0 and args.nesig_warmup_steps > 0:
        print(f"\n{'='*70}")
        print(f"NESIG WARMUP  ({args.nesig_warmup_steps} steps, student-calibrated difficulty)")
        print(f"{'='*70}\n")

        for warmup_step in range(1, args.nesig_warmup_steps + 1):
            print(f"\033[1m\033[93m[WARMUP] Step {warmup_step}/{args.nesig_warmup_steps}\033[0m")

            with torch.no_grad():
                problems, problem_info_list, trajectories, _, _ = \
                    nesig_trainer._generate_problems_and_trajectories(
                        args.num_problems_train,
                        args.max_init_actions_train,
                        args.max_goal_actions_train,
                    )

            consistent = sum(1 for p in problem_info_list if p['consistency'])
            print(f"  Consistent: {consistent}/{len(problem_info_list)}")

            # Save consistent problems to temp dir for student to load
            if consistent > 0:
                import tempfile
                with tempfile.TemporaryDirectory() as tmp_dir:
                    consistent_nesig_problems = [
                        p for p, info in zip(problems, problem_info_list)
                        if info['consistency']
                    ]
                    for i, p in enumerate(consistent_nesig_problems):
                        with open(Path(tmp_dir) / f'problem_{i}.pddl', 'w') as f:
                            f.write(p.dump_to_pddl(f'problem_{i}'))

                    warmup_student_problems = load_problems_from_dir(
                        tmp_dir, args.domain_path,
                        len(consistent_nesig_problems),
                        max_actions=args.max_actions_train,
                    )

                # Student solves warmup problems — no PPO update
                with torch.no_grad():
                    _, warmup_problem_info, _, _ = \
                        student_trainer._solve_and_collect_trajectories(
                            warmup_student_problems, args.max_actions_train
                        )

                warmup_difficulty_rewards = difficulty_evaluator.get_difficulty(warmup_problem_info)

                # Inject into NeSIG trajectories
                consistent_indices = [
                    i for i, info in enumerate(problem_info_list) if info['consistency']
                ]
                for traj_i, diff_reward in zip(consistent_indices, warmup_difficulty_rewards):
                    if trajectories[traj_i]:
                        trajectories[traj_i][-1]['difficulty_reward'] = diff_reward

            # Update NeSIG only — student does NOT train
            with torch.no_grad():
                init_trajectories, goal_trajectories = nesig_trainer._process_trajectories(
                    trajectories, problem_info_list,
                    train_init_policy=True,
                    train_goal_policy=True,
                )
            nesig_trainer._perform_train_step(init_policy, init_trajectories)
            nesig_trainer._perform_train_step(goal_policy, goal_trajectories)

        print(f"\n  Warmup complete. Starting co-training.\n")

    # ---- Replay buffer ----
    replay_buffer = ReplayBuffer(max_size=args.replay_buffer_size)
    replay_buffer.load(experiment_folder_path)

    # ---- Test set (generated before training) ----
    test_problems_dir = Path(args.test_problems_dir)
    if args.generate_test_problems:
        print(f"\nGenerating test problems into {test_problems_dir}...")
        generate_problems(
            args.generator_path, str(test_problems_dir),
            args.num_problems_test,
            args.test_min_blocks, args.test_max_blocks,
            seed_start=999454,
        )
    elif not list(test_problems_dir.glob('*.pddl')):
        raise FileNotFoundError(
            f"No .pddl files found in {test_problems_dir}. "
            f"Use --generate-test-problems to generate them."
        )
    else:
        print(f"\nUsing existing test problems from {test_problems_dir}")

    # If not generating, use the first num_problems of the folder
    available = len(list(test_problems_dir.glob('*.pddl')))
    if args.generate_test_problems:
        num_test = args.num_problems_test
    else:
        num_test = min(args.num_problems_test, available)
        if available > args.num_problems_test:
            print(f"  Note: {available} problems available, loading {num_test} "
                  f"(capped by --num-problems-test)")
        elif available < args.num_problems_test:
            print(f"  Warning: only {available} problems available, "
                  f"requested {args.num_problems_test}")
    print(f"  Loading {num_test} test problems")

    test_problems = load_problems_from_dir(
        str(test_problems_dir), args.domain_path,
        num_test,
        max_actions=args.max_actions_test,
    )

    print(f"\n{'='*70}")
    print(f"CO-TRAINING  NeSIG teacher + student")
    print(f"Steps      : {last_train_it + 1} -> {args.steps}")
    print(f"Teacher    : updates every {args.teacher_update_period} student iterations")
    print(f"Test       : every {args.test_period} steps ({num_test} problems)")
    print(f"{'='*70}\n")

    current_step = last_train_it + 1

    # Initialize problem cache before the loop
    consistent_problems = []
    cached_step_problem_dir = None

    while current_step <= args.steps:
        print(f"\033[1m\033[94mStep {current_step}/{args.steps}\033[0m")

        # ------------------------------------------------------------------
        # 1. Teacher generates problems (every problem_generation_period steps)
        # ------------------------------------------------------------------
        should_generate = (
            not consistent_problems or
            current_step % args.problem_generation_period == 0
        )

        if should_generate:
            print(f"\033[1m\033[93m[1] TEACHER GENERATES PROBLEMS\033[0m")
            print(f"  Generating {args.num_problems_train} consistent problems...")
            consistent_problems, consistent_infos, consistent_trajectories = \
                accumulate_consistent_problems(
                    nesig_trainer=nesig_trainer,
                    target=args.num_problems_train,
                    init_actions=args.max_init_actions_train,
                    goal_actions=args.max_goal_actions_train,
                    max_attempts=args.max_generation_attempts,
                )

            if not consistent_problems:
                print("  No consistent problems generated after max attempts, skipping step.")
                current_step += 1
                continue

            # Save to disk only when newly generated
            step_problem_dir = Path(args.data_dir) / f'step_{current_step}'
            step_problem_dir.mkdir(parents=True, exist_ok=True)
            for i, p in enumerate(consistent_problems):
                with open(step_problem_dir / f'problem_{i}.pddl', 'w') as f:
                    f.write(p.dump_to_pddl(f'problem_{i}'))
            replay_buffer.register_dir(str(step_problem_dir))
            cached_step_problem_dir = step_problem_dir
        else:
            print(f"\033[1m\033[93m[1] REUSING CACHED PROBLEMS (next generation at step "
                  f"{current_step + (args.problem_generation_period - current_step % args.problem_generation_period)})\033[0m")
            step_problem_dir = cached_step_problem_dir

        # ------------------------------------------------------------------
        # 2. Student loads problems
        # ------------------------------------------------------------------
        print(f"\033[1m\033[93m[2] STUDENT LOADS PROBLEMS\033[0m")

        # TODO: Check side-effects
        # NeSIG problems without replay — for clean difficulty signal
        nesig_only_problems = load_problems_from_dir(
            str(step_problem_dir), args.domain_path,
            len(consistent_problems),
            max_actions=args.max_actions_train,
        )

        # Student problems with extra replay problems added on top
        student_problems = load_problems_from_dir(
            str(step_problem_dir), args.domain_path,
            len(consistent_problems),
            max_actions=args.max_actions_train,
            replay_buffer=replay_buffer,
            replay_extra=args.replay_extra,
        )

        # ------------------------------------------------------------------
        # 3. Student attempts problems → trajectories + difficulty signal
        #    (BEFORE PPO update so difficulty is unbiased)
        # ------------------------------------------------------------------
        print(f"\033[1m\033[93m[3] STUDENT SOLVES + DIFFICULTY\033[0m")

        # Trajectories with replay buffer for student
        with torch.no_grad():
            _, problem_info, trajectories, _ = \
                student_trainer._solve_and_collect_trajectories(
                    student_problems, args.max_actions_train
                )
            
        # Trajectories without replay buffer for nesig feedback    
        with torch.no_grad():
            _, nesig_problem_info, _, _ = \
                student_trainer._solve_and_collect_trajectories(
                    nesig_only_problems, args.max_actions_train
                )

        new_difficulty_rewards = difficulty_evaluator.get_difficulty(nesig_problem_info)

        num_solved = sum(1 for d in new_difficulty_rewards if d > 0)
        mean_diff = sum(new_difficulty_rewards) / len(new_difficulty_rewards) \
            if new_difficulty_rewards else 0
        print(f"  [NESIG-STUDENT METRICS]")
        print(f"    Consistency rate : {len(consistent_problems)}/{args.num_problems_train}")
        print(f"    Student solved   : {num_solved}/{len(new_difficulty_rewards)}")
        print(f"    Mean difficulty  : {mean_diff:.3f}  (0=trivial, 1=hard, penalty=failed)")

        # Inject difficulty into NeSIG trajectories
        for traj, diff_reward in zip(consistent_trajectories, new_difficulty_rewards):
            if traj:
                traj[-1]['difficulty_reward'] = diff_reward

        # ------------------------------------------------------------------
        # 4. Student PPO update
        # ------------------------------------------------------------------
        print(f"\033[1m\033[93m[4] STUDENT PPO UPDATE\033[0m")
        samples = student_trainer._process_trajectories(trajectories, problem_info)
        if len(samples) >= args.min_samples_train:
            student_trainer._perform_train_step(samples)
            student_trainer.save_policy(save_best=False)
            student_trainer.policy.curr_logging_it += 1
            if current_step % args.log_period == 0:
                with torch.no_grad():
                    student_trainer.log_metrics(
                        'train', current_step, problem_info, trajectories=trajectories
                    )
            if test_problems and args.test_period != -1 \
                    and current_step % args.test_period == 0:
                with torch.no_grad():
                    _, test_info, _, _ = student_trainer._solve_and_collect_trajectories(
                        test_problems, args.max_actions_test
                    )
                test_metrics = student_trainer.log_metrics('test', current_step, test_info)
                print(f"  \033[1m\033[95m[TEST step {current_step}]\033[0m "
                      f"success={test_metrics['Success rate']:.1%}  "
                      f"efficiency={test_metrics['Mean efficiency']:.3f}  "
                      f"solved={int(test_metrics['Num successful'])}/{len(test_problems)}")
        else:
            print(f"    Skipping PPO: {len(samples)} < {args.min_samples_train}")

        # ------------------------------------------------------------------
        # 5. Teacher PPO update (every teacher_update_period steps)
        # ------------------------------------------------------------------
        if current_step % args.teacher_update_period == 0:
            print(f"\033[1m\033[93m[5] TEACHER PPO UPDATE\033[0m")
            with torch.no_grad():
                init_trajectories, goal_trajectories = nesig_trainer._process_trajectories(
                    consistent_trajectories, consistent_infos,
                    train_init_policy=True,
                    train_goal_policy=True,
                )
            nesig_trainer._perform_train_step(init_policy, init_trajectories)
            nesig_trainer._perform_train_step(goal_policy, goal_trajectories)

        # ------------------------------------------------------------------
        # Checkpointing
        # ------------------------------------------------------------------
        print(f"\033[1m\033[90mCHECKPOINTING\033[0m")
        replay_buffer.save(experiment_folder_path)
        save_experiment_info(experiment_info_path, args, experiment_id, current_step)

        # Save NeSIG policy checkpoints
        nesig_ckpt_dir = experiment_folder_path / 'nesig' / 'checkpoints'
        for name, policy_obj in [('init', init_policy), ('goal', goal_policy)]:
            save_policy_checkpoint(policy_obj, nesig_ckpt_dir / f'{name}_last.ckpt')

        current_step += 1

    # Evaluate on test set at the end of training
    print(f"\n  [FINAL TEST]")
    with torch.no_grad():
        _, test_info, _, _ = student_trainer._solve_and_collect_trajectories(
            test_problems, args.max_actions_test
        )
    test_metrics = student_trainer.log_metrics('test', current_step, test_info)
    print(f"  success={test_metrics['Success rate']:.1%}  "
        f"efficiency={test_metrics['Mean efficiency']:.3f}  "
        f"solved={int(test_metrics['Num successful'])}/{len(test_problems)}")

    student_trainer.close_writers()

    print(f"\n{'='*70}")
    print(f"Co-training complete.")
    print(f"{'='*70}\n")


# =====================================================================
# Entry Point
# =====================================================================

def main(args):
    os.chdir(dirname(dirname(dirname(dirname(abspath(__file__))))))
    seed_everything(args.seed, workers=True)

    experiment_id = get_experiment_id(args)
    print(f"\n>>> Experiment ID: {experiment_id}\n")

    experiment_folder_path = Path(args.experiments_dir) / experiment_id

    train(args, experiment_id, experiment_folder_path)
    
    # TODO: El test está integrado en train, cambiarlo 

    print("\n>>> Done!")
    print(f">>> Experiment ID: {experiment_id}\n")


if __name__ == '__main__':
    args = parse_arguments()
    args = validate_args(args)
    main(args)