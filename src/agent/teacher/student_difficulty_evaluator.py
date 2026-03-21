"""
> student_difficulty_evaluator.py

Replaces NeSIG's PlannerEvaluator with a student-based difficulty evaluator.
Instead of measuring difficulty via a planner, difficulty is measured by how
hard it is for the student agent to solve the problem:

    - If the student solves it:  difficulty = num_steps / max_actions  (in [0, 1])
    - If the student fails:      difficulty = penalty (fixed negative value)

This class follows the DifficultyEvaluator interface from NeSIG so it can be
dropped in as a direct replacement inside ProblemGenerator.
"""

from typing import List, Dict
import math

from src.nesig.metrics.difficulty import DifficultyEvaluator
from src.nesig.symbolic.pddl_problem import PDDLProblem as NeSIGProblem

from src.agent.controller.train_and_test_ACG import load_problems_from_dir


class StudentDifficultyEvaluator(DifficultyEvaluator):
    """
    Evaluates problem difficulty using the student agent's performance.

    Parameters
    ----------
    student_solver : ProblemSolver
        The student's ProblemSolver instance.
    penalty : float
        Difficulty reward when the student fails. Should be negative (e.g. -1.0).
    """

    def __init__(self, max_actions: int, penalty: float = 0,
                target_difficulty: float = 0.7, sigma: float = 0.2):
        self.max_actions = max_actions
        self.penalty = penalty
        self.target_difficulty = target_difficulty
        self.sigma = sigma

    def get_difficulty(self, problem_info_list: List[Dict]) -> List[float]:
        """
        Reward NeSIG for generating problems in the student's zone of proximal
        development — challenging but solvable. Uses a bell curve centered at
        target_difficulty to reward problems where the student uses ~70% of
        its action budget.

            - Too easy (student uses <30% budget)  → low reward
            - Just right (student uses ~70% budget) → high reward  
            - Too hard but solved (>90% budget)     → medium reward
            - Failed                                → penalty
        """
        rewards = []
        for info in problem_info_list:
            if info['goal_reached']:
                max_actions = info.get('max_actions', self.max_actions)
                diff = info['num_steps'] / max_actions  # in (0, 1]

                # Bell curve centered at target_difficulty
                # reward = exp(-((diff - target)^2) / (2 * sigma^2))
                target = self.target_difficulty  # e.g. 0.7
                sigma = self.sigma               # e.g. 0.2
                reward = math.exp(-((diff - target) ** 2) / (2 * sigma ** 2))
                rewards.append(reward)
            else:
                rewards.append(self.penalty)
        return rewards