"""
> train_teacher_only.py

Script for calibrating the NeSIG teacher against a FIXED student checkpoint.
The student does NOT train — only NeSIG updates.

Purpose: find good NeSIG hyperparameters (lr, ppo_epochs, init/goal actions,
difficulty reward shape) before running full co-training.

Usage:
    python -m src.agent.controller.train_teacher_only \
        --domain-path data/domains/blocksworld.pddl \
        --student-checkpoint experiments/0b3e3f89/checkpoints/last.ckpt \
        --device gpu \
        --seed 1 \
        --steps 200 \
        --num-problems-train 25 \
        --max-init-actions-train 10 \
        --max-goal-actions-train 10 \
        --nesig-lr 1e-3 \
        --nesig-ppo-epochs 3 \
        --difficulty-penalty -1.0 \
        --train-mode supersede
"""

import argparse
import hashlib
import json
import math
import os
import shutil
import tempfile
import torch
from copy import deepcopy
from pathlib import Path
from os.path import dirname, abspath
from typing import List, Optional, Tuple
from pytorch_lightning import seed_everything
from lifted_pddl import Parser
from torch.utils.tensorboard import SummaryWriter

# ---- NeSIG imports ----
from src.nesig.constants import DOMAIN_INFO
from src.nesig.learning.generative_policy import PPOPolicy
from src.nesig.learning.model_wrapper import NLMWrapperActor, NLMWrapperCritic
from src.nesig.symbolic.problem_generator import ProblemGenerator
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
    remove_if_exists, EXCLUDED_ARGS_ID, ID_LENGTH, ADDITIONAL_EXPERIMENT_INFO,
)
from src.agent.learning.generative_policy import PPOSolverPolicy
from src.agent.learning.model_wrapper import (
    NLMWrapperActor as StudentNLMWrapperActor,
    NLMWrapperCritic as StudentNLMWrapperCritic,
)
from src.agent.pddl.problem_solver import ProblemSolver
from src.agent.controller.trainer import PolicyTrainer as StudentTrainer

from src.agent.controller.train_and_test_ACG import (
    load_problems_from_dir, create_policy, save_experiment_info, read_last_train_it,
)
from src.agent.teacher.student_difficulty_evaluator import StudentDifficultyEvaluator


# =====================================================================
# Argument Parsing
# =====================================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Calibrate NeSIG teacher against a fixed student checkpoint.",
    )

    # ---- Domain ----
    parser.add_argument('--domain-path', type=str, required=True)
    parser.add_argument('--nesig-domain', type=str, default='blocksworld',
                        choices=tuple(DOMAIN_INFO.keys()))

    # ---- Fixed student ----
    parser.add_argument('--student-checkpoint', type=str, required=True,
                        help="Path to student last.ckpt to use as fixed reference")
    parser.add_argument('--reward-goal-reached', type=float, default=1.0)
    parser.add_argument('--reward-step', type=float, default=-1.0)
    parser.add_argument('--max-actions-train', type=int, default=None,
                        help="Action budget for student (defaults to 4*(test_max_blocks-1))")
    parser.add_argument('--test-max-blocks', type=int, default=30)

    # ---- NeSIG teacher ----
    parser.add_argument('--max-init-actions-train', type=int, default=10)
    parser.add_argument('--max-goal-actions-train', type=int, default=10)
    parser.add_argument('--nesig-ppo-epochs', type=int, default=3)
    parser.add_argument('--nesig-lr', type=float, default=1e-3)
    parser.add_argument('--diversity-threshold', type=float, default=0.25)
    parser.add_argument('--perc-problems-diversity', type=float, default=1.0)
    parser.add_argument('--r-eventual-consistency', type=float, default=-1.0)
    parser.add_argument('--consistency-evaluator', choices=('dummy', 'domain'),
                        default='domain')

    # ---- Difficulty reward ----
    parser.add_argument('--difficulty-penalty', type=float, default=0,
                        help="Reward for NeSIG when student fails the problem")
    parser.add_argument('--difficulty-target', type=float, default=0.7,
                        help="Target fraction of action budget student should use")
    parser.add_argument('--difficulty-sigma', type=float, default=0.2,
                        help="Width of bell curve around target difficulty")

    # ---- Training ----
    parser.add_argument('--steps', type=int, default=200,
                        help="Number of teacher-only training steps")
    parser.add_argument('--num-problems-train', type=int, default=25)
    parser.add_argument('--max-generation-attempts', type=int, default=30)
    parser.add_argument('--min-samples-train', type=int, default=10)
    parser.add_argument('--batch-size', type=int, default=64)
    parser.add_argument('--grad-clip', type=float, default=0.5)
    parser.add_argument('--critic-loss-weight', type=float, default=0.1)

    # ---- Setup ----
    parser.add_argument('--seed', type=int, default=1)
    parser.add_argument('--device', type=str, choices=('gpu', 'cpu'), default='gpu')
    parser.add_argument('--log-period', type=int, default=1)
    parser.add_argument('--experiments-dir', type=str, default='./experiments/teacher_calibration')
    parser.add_argument('--train-mode', choices=('supersede', 'resume'), default='resume')

    # ---- NLM model args (needed to rebuild student architecture) ----
    StudentNLMWrapperActor.add_model_specific_args(parser)
    PPOSolverPolicy.add_model_specific_args(parser)

    return parser.parse_args()


def validate_args(args):
    if args.steps < 1:
        raise ValueError("--steps must be > 0")
    if args.grad_clip == -1:
        args.grad_clip = None
    elif args.grad_clip <= 0:
        raise ValueError("--grad-clip must be > 0 or -1")
    if args.max_actions_train is None:
        args.max_actions_train = 4 * (args.test_max_blocks - 1)
    args.domain_path = str(Path(args.domain_path).resolve())
    if not Path(args.domain_path).exists():
        raise ValueError(f"Domain file not found: {args.domain_path}")
    if not Path(args.student_checkpoint).exists():
        raise ValueError(f"Student checkpoint not found: {args.student_checkpoint}")
    args.policy_type = 'PPO'
    args.train_mode = args.train_mode  # keep for create_policy compatibility
    return args


def get_experiment_id(args):
    excluded = set(EXCLUDED_ARGS_ID) | {'student_checkpoint'}
    included = {k: v for k, v in vars(args).items() if k not in excluded}
    return hashlib.sha256(str(included).encode()).hexdigest()[:ID_LENGTH]


# =====================================================================
# Checkpoint helper (copied from train_and_test_NeSIG)
# =====================================================================

def save_policy_checkpoint(policy_obj, ckpt_path: Path) -> None:
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
# Build components
# =====================================================================

def build_nesig_components(args, device):
    from src.nesig.controller.train_and_test import parse_domain_and_obtain_info

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
        num_problems_test=args.num_problems_train,
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
        init_term_action_prob=0.0,
        init_lr=args.nesig_lr,
        init_PPO_epochs=args.nesig_ppo_epochs,
        init_epsilon=0.2,
        init_entropy_coeffs=0.0,
        init_lifted_entropy_weight=0.5,
        goal_term_action_prob=0.0,
        goal_lr=args.nesig_lr,
        goal_PPO_epochs=args.nesig_ppo_epochs,
        goal_epsilon=0.2,
        goal_entropy_coeffs=0.0,
        goal_lifted_entropy_weight=0.5,
    )

    for attr, value in vars(args).items():
        if not hasattr(nesig_args, attr):
            setattr(nesig_args, attr, value)

    parsed_domain_info = parse_domain_and_obtain_info(nesig_args)

    init_actor_args = {'dummy_pddl_state': parsed_domain_info['dummy_state_init']}
    goal_actor_args = {'dummy_pddl_state': parsed_domain_info['dummy_state_goal']}

    init_policy = PPOPolicy(
        phase='init', args=nesig_args,
        actor_class=NLMWrapperActor, actor_arguments=init_actor_args,
        critic_class=NLMWrapperCritic, critic_arguments=deepcopy(init_actor_args),
        device=device,
    )
    goal_policy = PPOPolicy(
        phase='goal', args=nesig_args,
        actor_class=NLMWrapperActor, actor_arguments=goal_actor_args,
        critic_class=NLMWrapperCritic, critic_arguments=deepcopy(goal_actor_args),
        device=device,
    )

    diversity_evaluator = InitGoalDiversityEvaluator(
        r_diversity_weight=1.0,
        perc_problems_diversity=args.perc_problems_diversity,
    )

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


def build_frozen_student(args, domain_parser, device):
    """Load student from checkpoint and freeze all parameters."""
    # Use train_mode=resume + last_train_it>0 so create_policy loads the ckpt
    # We fake the experiment folder as the checkpoint's parent parent
    ckpt_path = Path(args.student_checkpoint)
    experiment_folder_path = ckpt_path.parent.parent  # experiments/<id>

    # Override train_mode temporarily so create_policy loads the checkpoint
    original_train_mode = args.train_mode
    args.train_mode = 'resume'
    student_policy = create_policy(
        args, domain_parser,
        last_train_it=1,  # > 0 so create_policy loads ckpt
        experiment_folder_path=experiment_folder_path,
        device=device,
    )
    args.train_mode = original_train_mode

    # Freeze all parameters — student will NOT be updated
    for param in student_policy.parameters():
        param.requires_grad = False
    student_policy.eval()

    student_solver = ProblemSolver(
        domain_parser, student_policy,
        reward_goal_reached=args.reward_goal_reached,
        reward_step=args.reward_step,
    )

    print(f"  Frozen student loaded from {ckpt_path}")
    print(f"  Student parameters: {sum(p.numel() for p in student_policy.parameters())}")

    return student_policy, student_solver


# =====================================================================
# Main
# =====================================================================

def train(args, experiment_id, experiment_folder_path: Path):
    experiment_info_path = experiment_folder_path / EXPERIMENT_INFO_FILENAME
    experiment_folder_path.mkdir(parents=True, exist_ok=True)

    last_step = 0
    if experiment_info_path.exists():
        with open(experiment_info_path) as f:
            last_step = json.load(f).get('last_train_it', 0)

    if args.train_mode == 'supersede':
        remove_if_exists(experiment_folder_path / LOGS_FOLDER_NAME)
        remove_if_exists(experiment_folder_path / CKPTS_FOLDER_NAME)
        last_step = 0

    # Save experiment info
    info = {k: v for k, v in vars(args).items() if k not in EXCLUDED_ARGS_ID}
    info['experiment_id'] = experiment_id
    info['last_train_it'] = last_step
    info.update(ADDITIONAL_EXPERIMENT_INFO)
    with open(experiment_info_path, 'w') as f:
        json.dump(info, f, indent=2)

    device = torch.device('cuda' if args.device == 'gpu' else 'cpu')

    # ---- Build frozen student ----
    print(f"\nLoading frozen student from {args.student_checkpoint}...")
    domain_parser = Parser()
    domain_parser.parse_domain(args.domain_path)
    student_policy, student_solver = build_frozen_student(args, domain_parser, device)
    if device.type == 'cuda':
        student_policy.to('cuda')

    # ---- Build NeSIG ----
    print(f"Building NeSIG teacher...")
    nesig_args, parsed_domain_info, init_policy, goal_policy, problem_generator = \
        build_nesig_components(args, device)

    # ---- Difficulty evaluator ----
    difficulty_evaluator = StudentDifficultyEvaluator(
        max_actions=args.max_actions_train,
        penalty=args.difficulty_penalty,
        target_difficulty=args.difficulty_target,
        sigma=args.difficulty_sigma,
    )

    # ---- Build trainers ----
    # StudentTrainer is only used for _solve_and_collect_trajectories
    student_trainer = StudentTrainer(
        args, experiment_folder_path, student_solver, student_policy, device
    )
    nesig_trainer = NeSIGTrainer(
        nesig_args, experiment_folder_path / 'nesig',
        problem_generator, init_policy, goal_policy, device=device,
    )

    # ---- Load NeSIG checkpoints on resume ----
    nesig_ckpt_dir = experiment_folder_path / 'nesig' / 'checkpoints'
    if args.train_mode == 'resume' and last_step > 0:
        init_ckpt = nesig_ckpt_dir / 'init_last.ckpt'
        goal_ckpt = nesig_ckpt_dir / 'goal_last.ckpt'
        if init_ckpt.exists() and goal_ckpt.exists():
            print(f"  Resuming NeSIG from {nesig_ckpt_dir}")
            init_policy.load_state_dict(
                torch.load(str(init_ckpt), map_location=device)['state_dict'])
            goal_policy.load_state_dict(
                torch.load(str(goal_ckpt), map_location=device)['state_dict'])
        else:
            print(f"  Warning: NeSIG checkpoints not found, starting from scratch")

    # ---- TensorBoard writer ----
    writer = SummaryWriter(log_dir=str(experiment_folder_path / LOGS_FOLDER_NAME / 'teacher'))

    print(f"\n{'='*70}")
    print(f"TEACHER CALIBRATION  (student frozen)")
    print(f"Student checkpoint : {args.student_checkpoint}")
    print(f"Steps              : {last_step + 1} -> {args.steps}")
    print(f"Max init actions   : {args.max_init_actions_train}")
    print(f"Max goal actions   : {args.max_goal_actions_train}")
    print(f"Difficulty target  : {args.difficulty_target} ± {args.difficulty_sigma}")
    print(f"Difficulty penalty : {args.difficulty_penalty}")
    print(f"{'='*70}\n")

    current_step = last_step + 1

    while current_step <= args.steps:
        print(f"\033[1m\033[94mStep {current_step}/{args.steps}\033[0m")

        # ------------------------------------------------------------------
        # 1. NeSIG generates problems
        # ------------------------------------------------------------------
        print(f"\033[1m\033[93m[1] TEACHER GENERATES PROBLEMS\033[0m")
        consistent_problems = []
        consistent_infos = []
        consistent_trajectories = []
        attempts = 0

        while len(consistent_problems) < args.num_problems_train \
                and attempts < args.max_generation_attempts:
            with torch.no_grad():
                problems, problem_info_list, trajectories, _, _ = \
                    nesig_trainer._generate_problems_and_trajectories(
                        args.num_problems_train,
                        args.max_init_actions_train,
                        args.max_goal_actions_train,
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

            if new_consistent:
                print(f"    attempt {attempts}/{args.max_generation_attempts}: "
                      f"{len(new_consistent)} consistent, "
                      f"total={len(consistent_problems)}/{args.num_problems_train}")
            else:
                print(f"    attempt {attempts}/{args.max_generation_attempts}: "
                      f"0 consistent")

        # Trim to target
        if len(consistent_problems) > args.num_problems_train:
            consistent_problems = consistent_problems[:args.num_problems_train]
            consistent_infos = consistent_infos[:args.num_problems_train]
            consistent_trajectories = consistent_trajectories[:args.num_problems_train]

        consistency_rate = len(consistent_problems) / args.num_problems_train

        if not consistent_problems:
            print("  No consistent problems generated, skipping step.")
            current_step += 1
            continue

        # ------------------------------------------------------------------
        # 2. Frozen student attempts problems → difficulty signal
        # ------------------------------------------------------------------
        print(f"\033[1m\033[93m[2] STUDENT SOLVES (frozen)\033[0m")

        with tempfile.TemporaryDirectory() as tmp_dir:
            for i, p in enumerate(consistent_problems):
                with open(Path(tmp_dir) / f'problem_{i}.pddl', 'w') as f:
                    f.write(p.dump_to_pddl(f'problem_{i}'))

            student_problems = load_problems_from_dir(
                tmp_dir, args.domain_path,
                len(consistent_problems),
                max_actions=args.max_actions_train,
            )

        with torch.no_grad():
            _, problem_info, _, _ = student_trainer._solve_and_collect_trajectories(
                student_problems, args.max_actions_train
            )

        difficulty_rewards = difficulty_evaluator.get_difficulty(problem_info)

        # Inject difficulty into NeSIG trajectories
        for traj, diff_reward in zip(consistent_trajectories, difficulty_rewards):
            if traj:
                traj[-1]['difficulty_reward'] = diff_reward

        # Metrics
        num_solved = sum(1 for info in problem_info if info['goal_reached'])
        fraction_solved = num_solved / len(problem_info) if problem_info else 0.0
        mean_diff = sum(difficulty_rewards) / len(difficulty_rewards) \
            if difficulty_rewards else 0.0
        mean_steps = sum(info['num_steps'] for info in problem_info) / len(problem_info) \
            if problem_info else 0.0
        mean_budget_used = sum(
            info['num_steps'] / args.max_actions_train
            for info in problem_info
        ) / len(problem_info) if problem_info else 0.0

        print(f"  Consistency rate : {consistency_rate:.1%} "
              f"({len(consistent_problems)}/{args.num_problems_train})")
        print(f"  Student solved   : {num_solved}/{len(problem_info)} "
              f"({fraction_solved:.1%})")
        print(f"  Mean diff reward : {mean_diff:.3f}")
        print(f"  Mean budget used : {mean_budget_used:.1%}")
        print(f"  Mean steps       : {mean_steps:.1f}/{args.max_actions_train}")

        # ------------------------------------------------------------------
        # 3. Teacher PPO update
        # ------------------------------------------------------------------
        print(f"\033[1m\033[93m[3] TEACHER PPO UPDATE\033[0m")
        with torch.no_grad():
            init_trajectories, goal_trajectories = nesig_trainer._process_trajectories(
                consistent_trajectories, consistent_infos,
                train_init_policy=True,
                train_goal_policy=True,
            )
        nesig_trainer._perform_train_step(init_policy, init_trajectories)
        nesig_trainer._perform_train_step(goal_policy, goal_trajectories)

        # ------------------------------------------------------------------
        # Logging
        # ------------------------------------------------------------------
        if current_step % args.log_period == 0:
            writer.add_scalar('Teacher/consistency_rate', consistency_rate,
                              global_step=current_step)
            writer.add_scalar('Teacher/fraction_solved', fraction_solved,
                              global_step=current_step)
            writer.add_scalar('Teacher/mean_difficulty_reward', mean_diff,
                              global_step=current_step)
            writer.add_scalar('Teacher/mean_budget_used', mean_budget_used,
                              global_step=current_step)
            writer.add_scalar('Teacher/mean_steps', mean_steps,
                              global_step=current_step)
            writer.add_scalar('Teacher/num_consistent', len(consistent_problems),
                              global_step=current_step)

        # ------------------------------------------------------------------
        # Checkpointing
        # ------------------------------------------------------------------
        for name, policy_obj in [('init', init_policy), ('goal', goal_policy)]:
            save_policy_checkpoint(policy_obj, nesig_ckpt_dir / f'{name}_last.ckpt')

        info['last_train_it'] = current_step
        with open(experiment_info_path, 'w') as f:
            json.dump(info, f, indent=2)

        current_step += 1

    writer.close()
    print(f"\n{'='*70}")
    print(f"Teacher calibration complete.")
    print(f"NeSIG checkpoints saved to {nesig_ckpt_dir}")
    print(f"{'='*70}\n")


def main(args):
    os.chdir(dirname(dirname(dirname(dirname(abspath(__file__))))))
    seed_everything(args.seed, workers=True)

    experiment_id = get_experiment_id(args)
    print(f"\n>>> Experiment ID: {experiment_id}\n")

    experiment_folder_path = Path(args.experiments_dir) / experiment_id
    train(args, experiment_id, experiment_folder_path)

    print("\n>>> Done!")
    print(f">>> Experiment ID: {experiment_id}\n")


if __name__ == '__main__':
    args = parse_arguments()
    args = validate_args(args)
    main(args)