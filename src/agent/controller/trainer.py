"""
> trainer.py

Training, validation and testing of solver policy.

Adapted from NeSIG's trainer.py but for PDDL problem SOLVING instead of GENERATION.
Key differences:
- Generates problems instead of using problem_generator
- One policy instead of init and goal policies
- Reward structure: step_penalty + goal_bonus + efficiency_bonus instead of consistency + difficulty + diversity
"""

from pathlib import Path
from typing import Tuple, List, Dict, Union, Optional
from random import randint
from copy import deepcopy
import os
import json
import numpy as np
import math
import torch
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
import pytorch_lightning as pl

from src.agent.constants import EXPERIMENT_INFO_FILENAME, LOGS_FOLDER_NAME, CKPTS_FOLDER_NAME, VAL_FOLDER_NAME, \
                                TEST_FOLDER_NAME, remove_if_exists
from src.agent.pddl.pddl_problem import PDDLProblem
from src.agent.pddl.problem_solver import ProblemSolver
from src.agent.learning.generative_policy import GenerativePolicy
from src.agent.learning.data_utils import SolverDataset, solver_collate_fn


class PolicyTrainer:
    """
    Class that encapsulates all functionality needed to train, validate and test a solver policy.
    
    It receives in the constructor a solver policy (either initialized from zero or loaded from a checkpoint).
    Then it can be used for training, validating, and testing the policy.
    
    Adapted from NeSIG's PolicyTrainer but for solving instead of generating.
    """

    def __init__(self, args, experiment_folder_path: Path, problem_solver: ProblemSolver,
                 policy: GenerativePolicy, device):
        """
        Initialize policy trainer.
        
        Parameters
        ----------
        args : argparse.Namespace
            Configuration arguments
        experiment_folder_path : Path
            Root experiment folder for logs, checkpoints, etc.
        problem_solver : ProblemSolver
            ProblemSolver instance used to solve and collect trajectories
        policy : GenerativePolicy
            Policy to train/validate/test
        device : torch.device
            Device to run on (CPU or CUDA)
        """
        self.args = args
        self.policy = policy
        self.problem_solver = problem_solver
        self.experiment_folder_path = experiment_folder_path

        # Using the paths in constants.py, obtain the paths for all the experiment files and subfolders
        self.experiment_info_path = experiment_folder_path / EXPERIMENT_INFO_FILENAME
        self.logs_folder = experiment_folder_path / LOGS_FOLDER_NAME
        self.ckpts_folder = experiment_folder_path / CKPTS_FOLDER_NAME
        self.val_folder = experiment_folder_path / VAL_FOLDER_NAME
        self.test_folder = experiment_folder_path / TEST_FOLDER_NAME

        # Obtain the corresponding torch.device from the args.device string
        self.device = device

    # =====================================================================
    # Trajectory Collection (from provided problems)
    # =====================================================================

    def _solve_and_collect_trajectories(self, problems: List[PDDLProblem], 
                                       max_actions: Union[int, Tuple[int, ...]]) -> Tuple:
        """
        Solve provided problems and collect trajectories.
        
        Similar to NeSIG's _generate_problems_and_trajectories but for solving.
        The main function is responsible for providing the problems.
        
        Parameters
        ----------
        problems : List[PDDLProblem]
            Problems to solve (provided by main function)
        max_actions : Union[int, Tuple[int, ...]]
            Action budget per problem. Either single int (same for all) or tuple 
            with one element per problem: max_actions[i] = budget for problem i
        
        Returns
        -------
        is_solved : List[bool]
            Whether each problem was solved
        problem_info_list : List[Dict]
            Problem info (success, efficiency, steps, etc.)
        trajectories : List[List[Dict]]
            Trajectories with populated rewards
        elapsed : float
            Total time for solving (seconds)
        """
        num_problems = len(problems)
        
        if num_problems == 0:
            return [], [], [], 0.0

        # TODO: Revisar que los budget los haga bien
        # Handle max_actions as either int or tuple of per-problem budgets
        if isinstance(max_actions, int):
            max_actions_list = max_actions
        else:
            # max_actions is a tuple/list with one element per problem
            assert len(max_actions) == num_problems, f"max_actions tuple must have {num_problems} elements (one per problem)"
            max_actions_list = tuple(max_actions) # NOTE: En NeSIG realmente usa números aleatorios, yo debería ajustar esto para que tenga tiempo suficiente de probar en los problemas

        # Solve problems and collect trajectories
        is_solved, problem_info_list, trajectories, elapsed = self.problem_solver.solve_problems(
            problems,
            list_max_actions=max_actions_list
        )

        return is_solved, problem_info_list, trajectories, elapsed

    # =====================================================================
    # Trajectory Processing (from NeSIG, adapted)
    # =====================================================================

    def _calculate_return_trajectories(self, trajectories: List[List[Dict]]) -> None:
        """
        Calculate discounted returns for each sample.
        Modifies trajectories in-place.
        
        Formula: R_t = r_t + gamma * R_{t+1}
        """
        for i in range(len(trajectories)):
            return_curr_state = 0  # R_t

            for j in range(len(trajectories[i]) - 1, -1, -1):
                reward = trajectories[i][j]['reward']
                return_curr_state = reward + self.args.disc_factor * return_curr_state

                trajectories[i][j]['return'] = return_curr_state  # R_t

    def _calculate_advantage_trajectories(self, policy: GenerativePolicy,
                                         trajectories: List[List[Dict]]) -> None:
        """
        Calculate advantages using GAE (Generalized Advantage Estimation).
        Modifies trajectories in-place.
        
        Formula: A_t = delta_t + (gamma*lambda)*A_{t+1}
        where delta_t = r_t + gamma*V(s_{t+1}) - V(s_t)
        """
        for i in range(len(trajectories)):
            if len(trajectories[i]) > 0:  # Skip empty trajectories
                # Calculate V(s) in parallel for all samples of the i-th trajectory
                internal_states = [sample['internal_state'] for sample in trajectories[i]]
                state_values, _ = policy.calculate_state_values(internal_states)
                state_values = [v.item() for v in state_values]  # Store as list of floats

                # Calculate advantage using GAE
                advantage_curr_state = trajectories[i][-1]['reward'] - state_values[-1] # A_final = r_final - V(s_final)
                trajectories[i][-1]['advantage'] = advantage_curr_state
                trajectories[i][-1]['state_value'] = state_values[-1]

                for j in range(len(trajectories[i]) - 2, -1, -1):
                    # delta_t = r_t + gamma*V(s_{t+1}) - V(s_t)
                    delta_curr_state = (trajectories[i][j]['reward'] + 
                                       self.args.disc_factor * state_values[j + 1] - 
                                       state_values[j])
                    # A_t = delta_t + (gamma*lambda)*A_{t+1}
                    advantage_curr_state = (delta_curr_state + 
                                           (self.args.disc_factor * self.args.gae_factor) * 
                                           advantage_curr_state)
                    trajectories[i][j]['advantage'] = advantage_curr_state
                    trajectories[i][j]['state_value'] = state_values[j]

    def _process_trajectories(self, trajectories: List[List[Dict]]) -> List[Dict]:
        """
        Process trajectories before training.
        
        Similar to NeSIG's _process_trajectories:
        1. Calculate returns
        2. Calculate advantages using GAE
        3. Flatten to samples
        
        Returns flattened list of samples.
        """
        self._calculate_return_trajectories(trajectories)
        self._calculate_advantage_trajectories(self.policy, trajectories)

        # Flatten trajectories to samples 
        # TODO: Revisar que cambio no rompa nada
        samples = []
        for trajectory in trajectories:
            samples.extend(trajectory)

        return samples

    # =====================================================================
    # Training Step (from NeSIG)
    # =====================================================================

    def _perform_train_step(self, samples: List[Dict]) -> None:
        """
        Execute one PPO training step.
        
        Similar to NeSIG's _perform_train_step.
        """
        # Skip training if not enough samples
        if len(samples) < self.args.min_samples_train:
            print(f"    Skipping PPO: {len(samples)} < {self.args.min_samples_train}")
            return

        print(f"    Performing PPO update with {len(samples)} samples")

        dataset = SolverDataset(samples)
        dataloader = DataLoader(
            dataset=dataset,
            batch_size=self.args.batch_size,
            shuffle=True,
            collate_fn=solver_collate_fn,
            num_workers=0
        )

        logger = pl.loggers.TensorBoardLogger(
            save_dir=self.logs_folder,
            name='train',
            version=''
        )

        grad_clip = self.args.grad_clip

        if self.device.type == 'cpu':
            trainer = pl.Trainer(
                max_epochs=self.args.solve_PPO_epochs,
                accelerator='cpu',
                enable_checkpointing=False,
                gradient_clip_val=grad_clip,
                logger=logger,
                enable_progress_bar=True,
            )
        else:
            trainer = pl.Trainer(
                max_epochs=self.args.solve_PPO_epochs,
                accelerator='cuda',
                devices=1,
                enable_checkpointing=False,
                gradient_clip_val=grad_clip,
                logger=logger,
                enable_progress_bar=True,
            )

        trainer.fit(self.policy, dataloader)

        # Move model back to GPU
        if self.device.type == 'cuda':
            self.policy.to('cuda')

    # =====================================================================
    # Checkpointing (from NeSIG)
    # =====================================================================

    def save_checkpoint(self, model: pl.LightningModule, ckpt_path: Path) -> None:
        """Save checkpoint using PyTorch Lightning."""
        remove_if_exists(ckpt_path)

        dummy_trainer = pl.Trainer(
            max_epochs=0,
            logger=False,
            enable_checkpointing=False,
            enable_progress_bar=False,
            enable_model_summary=False
        )
        dummy_trainer.fit(model, DataLoader(dataset=SolverDataset(), num_workers=0))
        dummy_trainer.save_checkpoint(str(ckpt_path))

        if self.device.type == 'cuda':
            model.to('cuda')

    def save_policy(self, save_best: bool = False) -> None:
        """Save policy checkpoint."""
        if save_best:
            ckpt_path = self.ckpts_folder / 'best.ckpt'
        else:
            ckpt_path = self.ckpts_folder / 'last.ckpt'

        self.save_checkpoint(self.policy, ckpt_path)

    # =====================================================================
    # Logging (adapted from NeSIG)
    # =====================================================================

    # TODO: Revisar métricas

    def log_metrics(self, phase: str, x_value: int, problem_info_list: List[Dict],
                   trajectories: List[List[Dict]] = None, score: Optional[float] = None) -> Dict:
        """
        Log metrics to Tensorboard.
        
        Similar to NeSIG's log_metrics but simplified for solver.
        
        Parameters
        ----------
        phase : str
            'train', 'val', or 'test'
        x_value : int
            x-axis value (iteration or problem size)
        problem_info_list : List[Dict]
            Problem info from solver
        trajectories : Optional[List[List[Dict]]]
            Trajectories (for train phase)
        score : Optional[float]
            Validation score (for val phase)
        
        Returns
        -------
        log_dict : Dict
            Dictionary of all logged metrics
        """
        assert phase in {'train', 'val', 'test'}, "phase must be 'train', 'val' or 'test'"

        writer = SummaryWriter(log_dir=self.logs_folder / phase)
        log_dict = dict()

        # ---- Problem metrics ----
        if problem_info_list:
            num_problems = len(problem_info_list)
            
            # Success rate
            success_count = sum(1 for p in problem_info_list if p.get('goal_reached', False))
            success_rate = success_count / num_problems if num_problems > 0 else 0.0
            
            # Efficiency stats (only for solved)
            successful = [p for p in problem_info_list if p.get('goal_reached', False)]
            if successful:
                mean_efficiency = sum(p['efficiency'] for p in successful) / len(successful)
                mean_steps = sum(p['num_steps'] for p in successful) / len(successful)
            else:
                mean_efficiency = 0.0
                mean_steps = 0.0
            
            # Mean steps for all
            mean_steps_all = sum(p['num_steps'] for p in problem_info_list) / num_problems
            
            log_dict['Success rate'] = success_rate
            log_dict['Mean efficiency'] = mean_efficiency
            log_dict['Mean steps (successful)'] = mean_steps if successful else 0.0
            log_dict['Mean steps (all)'] = mean_steps_all
            log_dict['Num successful'] = success_count
            
            writer.add_scalar('Success rate', success_rate, global_step=x_value)
            writer.add_scalar('Mean efficiency', mean_efficiency, global_step=x_value)
            writer.add_scalar('Mean steps (successful)', mean_steps, global_step=x_value)
            writer.add_scalar('Mean steps (all)', mean_steps_all, global_step=x_value)

        # ---- Trajectory metrics (train phase) ----
        if trajectories is not None and len(trajectories) > 0:
            samples = [s for traj in trajectories for s in traj]
            
            if samples:
                mean_return = sum(s['return'] for s in samples) / len(samples)
                mean_advantage = sum(s.get('advantage', 0.0) for s in samples) / len(samples)
                
                log_dict['Mean return'] = mean_return
                log_dict['Mean advantage'] = mean_advantage
                
                writer.add_scalar('Mean return', mean_return, global_step=x_value)
                writer.add_scalar('Mean advantage', mean_advantage, global_step=x_value)

        # ---- Validation score ----
        if score is not None:
            log_dict['Average score'] = score
            writer.add_scalar('Average score', score, global_step=x_value)

        # ---- GPU memory ----
        if phase == 'train' and self.device.type == 'cuda':
            mem_allocated = torch.cuda.memory_allocated(self.device) / 2**20
            log_dict['Allocated Memory (MB)'] = mem_allocated
            writer.add_scalar('Allocated Memory (MB)', mem_allocated, global_step=x_value)

        writer.close()
        return log_dict

    # =====================================================================
    # Validation (adapted from NeSIG)
    # =====================================================================

    def _run_validation(self, curr_train_it: int, best_val_score: float,
                       best_train_it: int, val_problems_fn) -> Tuple[float, int]:
        """
        Run validation epoch.
        
        Similar to NeSIG's _run_validation.
        """
        print(f"\n  Running validation...")

        with torch.no_grad():
            # Get validation problems and solve them
            val_problems = val_problems_fn()
            is_solved, val_problem_info, val_trajectories, val_elapsed = self._solve_and_collect_trajectories(
                val_problems,
                self.args.max_actions_val
            )

            # Validation score = success rate
            val_score = (sum(1 for p in val_problem_info if p['goal_reached']) / 
                        len(val_problem_info) if val_problem_info else 0.0)

            print(f"  Validation score: {val_score:.3f}")

            # Log validation metrics
            self.log_metrics('val', curr_train_it, val_problem_info, score=val_score)

            # Save best checkpoint
            if val_score > best_val_score:
                best_val_score = val_score
                best_train_it = curr_train_it
                self.save_policy(save_best=True)
                print(f"  ✓ New best validation score: {val_score:.3f}")
            else:
                self.save_policy(save_best=False)

        return best_val_score, best_train_it

    # =====================================================================
    # Main Training Loop (adapted from NeSIG)
    # =====================================================================

    def train_and_val(self, start_it: int, end_it: int, 
                      train_problems_fn, val_problems_fn) -> Tuple[int, int]:
        """
        Main training and validation loop.
        
        Similar to NeSIG's train_and_val but for solving.
        
        Parameters
        ----------
        start_it : int
            Starting iteration
        end_it : int
            Ending iteration
        train_problems_fn : callable
            Function that returns list of training problems when called
        val_problems_fn : callable
            Function that returns list of validation problems when called
        
        Returns
        -------
        best_train_it : int
            Iteration with best validation score
        last_train_it : int
            Last training iteration
        """
        print(f"\n{'='*70}")
        print(f"TRAINING SOLVER POLICY")
        print(f"Iterations: {start_it} -> {end_it}")
        print(f"{'='*70}\n")

        best_val_score = float('-inf')
        best_train_it = start_it

        if self.device.type == 'cuda':
            self.policy.to('cuda')

        curr_train_it = start_it
        while curr_train_it <= end_it:
            print(f"\nIteration {curr_train_it}/{end_it}")

            with torch.no_grad():
                # Get training problems and solve them
                train_problems = train_problems_fn()
                is_solved, problem_info, trajectories, elapsed = self._solve_and_collect_trajectories(
                    train_problems,
                    self.args.max_actions_train
                )

            if len(trajectories) == 0:
                print("  No trajectories collected")
                curr_train_it += 1
                continue

            # Process trajectories
            samples = self._process_trajectories(trajectories)

            # PPO training
            self._perform_train_step(samples)

            # Save last checkpoint
            self.save_policy(save_best=False)
            last_train_it = curr_train_it

            with torch.no_grad():
                # Logging
                if curr_train_it % self.args.log_period == 0:
                    self.log_metrics('train', curr_train_it, problem_info, trajectories=trajectories)

                # Validation
                if self.args.val_period != -1 and curr_train_it % self.args.val_period == 0:
                    best_val_score, best_train_it = self._run_validation(
                        curr_train_it, best_val_score, best_train_it, val_problems_fn
                    )

            curr_train_it += 1

        # Final validation if needed
        if self.args.val_period == -1 or ((curr_train_it - 1) % self.args.val_period) != 0:
            best_val_score, best_train_it = self._run_validation(
                curr_train_it - 1, best_val_score, best_train_it, val_problems_fn
            )

        print(f"\n{'='*70}")
        print(f"Training Complete!")
        print(f"  Best iteration: {best_train_it}")
        print(f"  Last iteration: {last_train_it}")
        print(f"{'='*70}\n")

        return best_train_it, last_train_it

    # =====================================================================
    # Testing (adapted from NeSIG)
    # =====================================================================

    def test(self, test_problems_fn) -> None:
        """
        Run test experiments.
        
        Similar to NeSIG's test method.
        
        Parameters
        ----------
        test_problems_fn : callable
            Function that returns list of test problems when called
        """
        print(f"\n{'='*70}")
        print(f"TESTING SOLVER POLICY")
        print(f"{'='*70}\n")

        self.test_folder.mkdir(parents=True, exist_ok=True)

        with torch.no_grad():
            # Get test problems and solve them
            test_problems = test_problems_fn()
            is_solved, test_problem_info, test_trajectories, test_elapsed = self._solve_and_collect_trajectories(
                test_problems,
                self.args.max_actions_test
            )

            # Compute test metrics
            success_count = sum(1 for p in test_problem_info if p['goal_reached'])
            success_rate = success_count / len(test_problem_info) if test_problem_info else 0.0

            successful = [p for p in test_problem_info if p['goal_reached']]
            mean_steps = sum(p['num_steps'] for p in successful) / len(successful) if successful else 0.0
            mean_efficiency = sum(p['efficiency'] for p in successful) / len(successful) if successful else 0.0

            print(f"Test Results:")
            print(f"  Success rate: {success_rate:.1%}")
            print(f"  Successful: {success_count}/{len(test_problem_info)}")
            print(f"  Mean steps: {mean_steps:.1f}")
            print(f"  Mean efficiency: {mean_efficiency:.3f}")

            # Save results
            test_results_path = self.test_folder / "results.json"
            test_results = {
                'success_rate': float(success_rate),
                'num_successful': int(success_count),
                'num_problems': len(test_problem_info),
                'mean_steps': float(mean_steps),
                'mean_efficiency': float(mean_efficiency),
                'elapsed_time': float(test_elapsed),
            }
            with open(test_results_path, 'w') as f:
                json.dump(test_results, f, indent=2)

            # Log test metrics
            self.log_metrics('test', 0, test_problem_info)

        print(f"\n{'='*70}")
        print(f"Testing Complete!")
        print(f"{'='*70}\n")