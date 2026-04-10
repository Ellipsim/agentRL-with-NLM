"""
> loss_difficulty_evaluator.py
"""

from typing import List, Tuple, Union
from pathlib import Path
from src.nesig.metrics.difficulty import DifficultyEvaluator as NeSIGDifficultyEvaluator
from src.nesig.symbolic.pddl_problem import PDDLProblem as NeSIGProblem

class StudentDifficultyEvaluator(NeSIGDifficultyEvaluator):
    """
    NeSIG-compatible difficulty evaluator backed by student PPO loss.

    Instead of caching rewards from the previous step, difficulty is now
    injected directly into NeSIG trajectories after the student PPO update,
    eliminating the one-step lag.

    Usage in training loop:
        1. NeSIG generates problems (difficulty_reward initialised to 0)
        2. Student solves problems
        3. Student PPO update
        4. Call inject_difficulty(policy, consistent_trajectories)
        5. NeSIG PPO update — trajectories now have correct difficulty rewards
    """

    plan_args = ['student']

    def __init__(self, difficulty_penalty: float = 0.0):
        self.difficulty_penalty = difficulty_penalty

    def inject_difficulty(self, per_problem_losses: List[float], nesig_trajectories: List[List[dict]]) -> float:
        """
        Inject per-problem critic losses as difficulty rewards into NeSIG trajectories.
        Must be called after _process_trajectories (losses already computed).

        Returns the mean difficulty reward for logging.
        """
        assert len(per_problem_losses) == len(nesig_trajectories), \
            "per_problem_losses and nesig_trajectories must be aligned (one per problem)"

        for loss, nesig_traj in zip(per_problem_losses, nesig_trajectories):
            if nesig_traj:
                nesig_traj[-1]['difficulty_reward'] = loss

        return sum(per_problem_losses) / len(per_problem_losses) if per_problem_losses else 0.0

    def get_difficulty(self, problem_list: List[Union[NeSIGProblem, Path]]) -> Tuple[List[dict], List[float]]:
        """
        Called by ProblemGenerator during generation.
        Returns 0 — difficulty is injected later via inject_difficulty().
        """
        n = len(problem_list)
        rewards = [self.difficulty_penalty] * n
        difficulties = [{'student': r} for r in rewards]
        return difficulties, rewards