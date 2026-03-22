"""
> student_difficulty_evaluator.py

Replaces NeSIG's PlannerEvaluator

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
        Difficulty reward when the student fails.
    """

    def __init__(self, max_actions: int, penalty: float = 0):
        self.max_actions = max_actions
        self.penalty = penalty

    def get_difficulty(self, problem_info_list: List[Dict]) -> List[float]:
        rewards = []
        for info in problem_info_list:
            if info['goal_reached']:
                max_actions = info.get('max_actions', self.max_actions)
                reward = info['num_steps'] / (max_actions / 4)
                rewards.append(reward)
            else:
                rewards.append(self.penalty)  # 0.0
        return rewards