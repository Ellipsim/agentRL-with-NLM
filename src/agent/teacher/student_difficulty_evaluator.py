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

    # TODO: Adjust penalty and difficulty reward

    def __init__(self, max_actions: int, penalty: float = 0.0):
        self.max_actions = max_actions
        self.penalty = penalty

    def get_difficulty(self, problem_info_list: List[Dict]) -> List[float]:
        """
        Compute difficulty rewards from student rollout info.

        Parameters
        ----------
        problem_info_list : List[Dict]
            Problem info returned by student_solver.solve_problems().
            Each dict must have 'goal_reached' and 'num_steps'.

        Returns
        -------
        difficulty_rewards : List[float]
            One reward per problem. In [0,1] if solved, penalty if failed.
        """
        rewards = []
        for info in problem_info_list:
            if info['goal_reached']:
                rewards.append(info['num_steps'] / self.max_actions)
            else:
                rewards.append(self.penalty)
        return rewards