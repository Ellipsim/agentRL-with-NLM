"""
> loss_difficulty_evaluator.py
"""

from typing import List, Tuple, Union
from pathlib import Path
from src.nesig.metrics.difficulty import DifficultyEvaluator as NeSIGDifficultyEvaluator
from src.nesig.symbolic.pddl_problem import PDDLProblem as NeSIGProblem


class LossBasedDifficultyEvaluator:
    def __init__(self, ema_alpha: float = 0.1,
                 critic_weight: float = 1, ppo_weight: float = 0):
        self.ema_alpha = ema_alpha
        self.critic_weight = critic_weight
        self.ppo_weight = ppo_weight
        self._ema_critic = None
        self._ema_ppo = None

    def get_difficulty(self, policy, num_problems: int) -> List[float]:
        critic_loss = getattr(policy, 'last_critic_loss', 0.0)
        ppo_loss = getattr(policy, 'last_ppo_loss', 0.0)

        if self._ema_critic is None:
            self._ema_critic = critic_loss + 1e-8
            self._ema_ppo = ppo_loss + 1e-8
        else:
            self._ema_critic = self.ema_alpha * critic_loss + (1 - self.ema_alpha) * self._ema_critic
            self._ema_ppo    = self.ema_alpha * ppo_loss    + (1 - self.ema_alpha) * self._ema_ppo

        norm_critic = min(critic_loss / (self._ema_critic + 1e-8), 2.0)
        norm_ppo    = min(ppo_loss    / (self._ema_ppo    + 1e-8), 2.0)

        difficulty = self.critic_weight * norm_critic + self.ppo_weight * norm_ppo
        return [difficulty] * num_problems

    def summary(self) -> dict:
        return {
            'ema_critic': self._ema_critic or 0.0,
            'ema_ppo':    self._ema_ppo or 0.0,
        }


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

    def __init__(self, loss_evaluator: LossBasedDifficultyEvaluator,
                 difficulty_penalty: float = 0.0):
        self._loss_evaluator = loss_evaluator
        self.difficulty_penalty = difficulty_penalty

    def inject_difficulty(self, policy, nesig_trajectories: List[List[dict]]) -> float:
        """
        Compute difficulty from student's latest losses and inject into
        the last sample of each NeSIG trajectory.

        Returns the mean difficulty reward for logging.
        """
        difficulty = self._loss_evaluator.get_difficulty(
            policy=policy,
            num_problems=len(nesig_trajectories),
        )[0]  # all same value

        for traj in nesig_trajectories:
            if traj:
                traj[-1]['difficulty_reward'] = difficulty

        return difficulty

    def get_difficulty(self, problem_list: List[Union[NeSIGProblem, Path]]) -> Tuple[List[dict], List[float]]:
        """
        Called by ProblemGenerator during generation.
        Returns 0 — difficulty is injected later via inject_difficulty().
        """
        n = len(problem_list)
        rewards = [self.difficulty_penalty] * n
        difficulties = [{'student': r} for r in rewards]
        return difficulties, rewards