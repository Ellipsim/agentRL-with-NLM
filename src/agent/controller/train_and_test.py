"""
> train_and_test.py

Main script for training, validating and testing the solver policy.

NOTE: This script should be executed as a module:
  python -m src.agent.controller.train_and_test

This script:
  1. Parses command-line arguments
  2. Trains the solver policy on problems
  3. Validates the policy
  4. Tests the policy on test problems

Key differences from NeSIG:
  - Problems are SOLVED, not generated
  - Single policy (not init + goal)
  - Simpler argument structure
  - No consistency/difficulty/diversity evaluators
"""

import argparse
import hashlib
import sys
import os
import torch
from os.path import dirname, abspath
from pathlib import Path
from pytorch_lightning import seed_everything
import json
from typing import Tuple, List, Dict, Optional
from lifted_pddl import Parser

from src.agent.constants import EXPERIMENT_INFO_FILENAME, LOGS_FOLDER_NAME, CKPTS_FOLDER_NAME, VAL_FOLDER_NAME, TEST_FOLDER_NAME, remove_if_exists, EXCLUDED_ARGS_ID, ID_LENGTH, ADDITIONAL_EXPERIMENT_INFO
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


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Train, validate and test a solver policy."
    )

    # ---- Domain and problem configuration ----
    parser.add_argument(
        '--domain-path', type=str, required=True,
        help="Path to domain.pddl file"
    )
    parser.add_argument(
        '--train-problems-dir', type=str, required=True,
        help="Directory containing training problems"
    )
    parser.add_argument(
        '--val-problems-dir', type=str, required=True,
        help="Directory containing validation problems"
    )
    parser.add_argument(
        '--test-problems-dir', type=str, required=True,
        help="Directory containing test problems"
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

    # ---- Training configuration ----
    parser.add_argument(
        '--steps', type=int, default=100,
        help="Number of training iterations"
    )
    parser.add_argument(
        '--num-problems-train', type=int, default=5,
        help="Number of problems to solve per training iteration"
    )
    parser.add_argument(
        '--max-actions-train', type=parse_max_actions, default=50,
        help="Action budget per training problem (int or tuple)"
    )
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

    # ---- Discounting and advantage estimation ----
    parser.add_argument(
        '--disc-factor', type=float, default=0.99,
        help="Discount factor (gamma) for returns"
    )
    parser.add_argument(
        '--gae-factor', type=float, default=0.95,
        help="GAE factor (lambda) for advantage estimation"
    )

    # ---- Validation configuration ----
    parser.add_argument(
        '--val-period', type=int, default=10,
        help="Training steps between validation epochs (-1 = only at end)"
    )
    parser.add_argument(
        '--num-problems-val', type=int, default=10,
        help="Number of problems per validation epoch"
    )
    parser.add_argument(
        '--max-actions-val', type=parse_max_actions, default=50,
        help="Action budget per validation problem"
    )

    # ---- Testing configuration ----
    parser.add_argument(
        '--num-problems-test', type=int, default=20,
        help="Number of problems per test"
    )
    parser.add_argument(
        '--max-actions-test', type=parse_max_actions, default=50,
        help="Action budget per test problem"
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
    parser.add_argument(
        '--raise-error-test', action='store_true',
        help="Raise error if test attempted without trained policy"
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
    # Register all NLM-specific arguments (breadth, depth, hidden-features, etc.)
    NLMWrapperActor.add_model_specific_args(parser)

    # ---- Critic loss weight (not in add_model_specific_args) ----
    parser.add_argument(
        '--critic-loss-weight', type=float, default=0.1,
        help="Weight for critic loss vs actor loss"
    )

    # ---- Add policy-specific arguments ----
    # This registers all --solve-* arguments for PPOSolverPolicy
    PPOSolverPolicy.add_model_specific_args(parser)

    args = parser.parse_args()
    return args


def validate_args(args):
    """Validate arguments."""
    if args.steps < 1:
        raise ValueError("--steps must be > 0")
    if args.num_problems_train < 1:
        raise ValueError("--num-problems-train must be > 0")
    if args.num_problems_val < 1:
        raise ValueError("--num-problems-val must be > 0")
    if args.num_problems_test < 1:
        raise ValueError("--num-problems-test must be > 0")
    if args.batch_size < 1:
        raise ValueError("--batch-size must be > 0")
    if args.min_samples_train < 1:
        raise ValueError("--min-samples-train must be > 0")
    if args.disc_factor < 0 or args.disc_factor > 1:
        raise ValueError("--disc-factor must be in [0, 1]")
    if args.gae_factor < 0 or args.gae_factor > 1:
        raise ValueError("--gae-factor must be in [0, 1]")
    if args.train_mode == "skip" and args.test_mode == "skip":
        raise ValueError("Cannot skip both training and testing")
    
    # Convert to absolute paths
    args.domain_path = str(Path(args.domain_path).resolve())
    args.train_problems_dir = str(Path(args.train_problems_dir).resolve())
    args.val_problems_dir = str(Path(args.val_problems_dir).resolve())
    args.test_problems_dir = str(Path(args.test_problems_dir).resolve())
    
    if not Path(args.domain_path).exists():
        raise ValueError(f"Domain file not found: {args.domain_path}")
    if not Path(args.train_problems_dir).exists():
        raise ValueError(f"Train problems dir not found: {args.train_problems_dir}")
    if not Path(args.val_problems_dir).exists():
        raise ValueError(f"Val problems dir not found: {args.val_problems_dir}")
    if not Path(args.test_problems_dir).exists():
        raise ValueError(f"Test problems dir not found: {args.test_problems_dir}")
    
    if args.grad_clip == -1:
        args.grad_clip = None
    elif args.grad_clip <= 0:
        raise ValueError("--grad-clip must be > 0 or -1")
    
    return args


# =====================================================================
# Experiment Management
# =====================================================================

def get_experiment_id(args):
    """Generate unique experiment ID from arguments."""
    included_args = {k: v for k, v in vars(args).items() if k not in EXCLUDED_ARGS_ID}
    full_hash = hashlib.sha256(str(included_args).encode()).hexdigest()[:ID_LENGTH]
    return full_hash


def save_experiment_info(filepath, args, experiment_id, best_train_it, last_train_it, best_val_score):
    """Save experiment metadata to JSON."""
    experiment_info = {k: v for k, v in vars(args).items() if k not in EXCLUDED_ARGS_ID}
    
    experiment_info['experiment_id'] = experiment_id
    experiment_info['best_train_it'] = best_train_it
    experiment_info['last_train_it'] = last_train_it
    experiment_info['best_val_score'] = best_val_score
    experiment_info.update(ADDITIONAL_EXPERIMENT_INFO)
    
    with open(filepath, 'w') as f:
        json.dump(experiment_info, f, indent=2)


def read_experiment_info(experiment_info_path):
    """Read previous experiment metadata."""
    if experiment_info_path.exists():
        with open(experiment_info_path, 'r') as f:
            info = json.load(f)
            return info.get('best_train_it', 0), info.get('last_train_it', 0), info.get('best_val_score', -1)
    return 0, 0, -1


# =====================================================================
# Problem Loading
# =====================================================================

def load_problems_from_dir(problem_dir, domain_path, num_problems, max_actions=None):
    """Load problems from directory with fresh parser for each problem."""
    problem_dir = Path(problem_dir)
    problem_files = sorted(problem_dir.glob("*.pddl"))
    
    if not problem_files:
        raise FileNotFoundError(f"No .pddl files in {problem_dir}")
    
    problems = []
    for i in range(num_problems):
        problem_file = problem_files[i % len(problem_files)]
        # Create a fresh parser for each problem to avoid duplicate constant errors
        fresh_parser = Parser()
        fresh_parser.parse_domain(str(domain_path))
        
        problem = PDDLProblem.load_from_pddl(fresh_parser, str(problem_file))
        if problem is not None:
            # Set max_actions if provided
            if max_actions is not None:
                if isinstance(max_actions, tuple):
                    problem.max_actions = max_actions[i % len(max_actions)]
                else:
                    problem.max_actions = max_actions
            problems.append(problem)
    
    return problems


# =====================================================================
# Policy Creation
# =====================================================================

# TODO: Es correcto tener las max action aquí?

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
        elif args.train_mode == "resume":
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
# Training and Testing
# =====================================================================

def train_and_val(args, parser, experiment_id, experiment_folder_path):
    """Train and validate the policy."""
    experiment_info_path = experiment_folder_path / EXPERIMENT_INFO_FILENAME
    
    # Create experiment folder
    experiment_folder_path.mkdir(parents=True, exist_ok=True)
    
    # Read previous progress
    best_train_it, last_train_it, best_val_score = read_experiment_info(experiment_info_path)
    
    print(f"Previous progress: best={best_train_it}, last={last_train_it}, score={best_val_score}")
    
    # Reset if superseding
    if args.train_mode == "supersede" or last_train_it == 0:
        remove_if_exists(experiment_folder_path / LOGS_FOLDER_NAME)
        remove_if_exists(experiment_folder_path / CKPTS_FOLDER_NAME)
        remove_if_exists(experiment_folder_path / VAL_FOLDER_NAME)
        remove_if_exists(experiment_folder_path / TEST_FOLDER_NAME)
        best_train_it = 0
        last_train_it = 0
        best_val_score = -1
    
    # Save experiment info
    save_experiment_info(experiment_info_path, args, experiment_id, best_train_it, last_train_it, best_val_score)
    
    # Skip if needed
    if args.train_mode == 'skip' or args.policy_type == 'random' or last_train_it >= args.steps:
        return
    
    # Remove test folder (best policy may have changed)
    remove_if_exists(experiment_folder_path / TEST_FOLDER_NAME)
    
    # Create policy
    device = torch.device("cuda" if args.device == 'gpu' else "cpu")
    policy = create_policy(args, parser, last_train_it, experiment_folder_path, device)
    
    # Create problem solver
    problem_solver = ProblemSolver(
        parser,
        policy,
        reward_goal_reached=args.reward_goal_reached,
        reward_step=args.reward_step,
        reward_efficiency=args.reward_efficiency
    )
    
    # Create trainer
    trainer = PolicyTrainer(args, experiment_folder_path, problem_solver, policy, device)
    
    # Define problem loading functions
    def get_train_problems():
        return load_problems_from_dir(
            args.train_problems_dir, 
            args.domain_path, 
            args.num_problems_train,
            max_actions=args.max_actions_train
        )
    
    def get_val_problems():
        return load_problems_from_dir(
            args.val_problems_dir, 
            args.domain_path, 
            args.num_problems_val,
            max_actions=args.max_actions_val
        )
    
    # Train
    best_train_it, last_train_it = trainer.train_and_val(
        start_it=last_train_it + 1,
        end_it=args.steps,
        train_problems_fn=get_train_problems,
        val_problems_fn=get_val_problems
    )
    
    # Save final progress
    save_experiment_info(experiment_info_path, args, experiment_id, best_train_it, last_train_it, best_val_score)


def test(args, parser, experiment_id, experiment_folder_path):
    """Test the trained policy."""
    if args.test_mode == 'skip':
        return
    
    experiment_info_path = experiment_folder_path / EXPERIMENT_INFO_FILENAME
    test_folder_path = experiment_folder_path / TEST_FOLDER_NAME
    
    # Read progress
    best_train_it, last_train_it, best_val_score = read_experiment_info(experiment_info_path)
    
    # Check if we have a trained policy
    if args.policy_type != 'random':
        ckpt_path = experiment_folder_path / CKPTS_FOLDER_NAME / 'best.ckpt'
        if not ckpt_path.exists():
            if args.raise_error_test:
                raise FileNotFoundError(f"Best checkpoint not found: {ckpt_path}")
            else:
                print("Skipping test: no trained policy found")
                return
    
    # Reset test if superseding
    if args.test_mode == 'supersede':
        remove_if_exists(test_folder_path)
    
    test_folder_path.mkdir(parents=True, exist_ok=True)
    
    # Load policy
    device = torch.device("cuda" if args.device == 'gpu' else "cpu")
    
    if args.policy_type == 'random':
        policy = RandomPolicy()
    else:
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
        
        actor_args = {'dummy_pddl_state': dummy_state}
        critic_args = {'dummy_pddl_state': dummy_state}
        
        # Convert args to dict
        args_dict = vars(args)
        
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
    
    # Create problem solver
    problem_solver = ProblemSolver(
        parser,
        policy,
        reward_goal_reached=args.reward_goal_reached,
        reward_step=args.reward_step,
        reward_efficiency=args.reward_efficiency
    )
    
    # Create trainer
    trainer = PolicyTrainer(args, experiment_folder_path, problem_solver, policy, device)
    
    # Define test problem loading
    def get_test_problems():
        return load_problems_from_dir(
            args.test_problems_dir, 
            args.domain_path, 
            args.num_problems_test,
            max_actions=args.max_actions_test
        )
    
    # Test
    trainer.test(test_problems_fn=get_test_problems)


def main(args):
    """Main entry point."""
    # Set working directory
    os.chdir(dirname(dirname(dirname(dirname(abspath(__file__))))))
    
    # Reproducibility
    seed_everything(args.seed, workers=True)
    
    # Get experiment ID
    experiment_id = get_experiment_id(args)
    print(f"\n>>> Experiment ID: {experiment_id}\n")
    
    # Setup experiment folder
    experiments_dir = Path(args.experiments_dir)
    experiment_folder_path = experiments_dir / experiment_id
    
    # Parse domain
    parser = Parser()
    parser.parse_domain(args.domain_path)
    
    # Train and validate
    train_and_val(args, parser, experiment_id, experiment_folder_path)
    
    # Test
    test(args, parser, experiment_id, experiment_folder_path)
    
    print("\n>>> Done!\n")


if __name__ == '__main__':
    args = parse_arguments()
    args = validate_args(args)
    main(args)