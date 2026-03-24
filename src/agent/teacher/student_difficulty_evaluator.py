"""

Difficulty reward for the NeSIG teacher based on structural problem complexity.
    
"""

from typing import List, Optional

# Internal import — complexity lives here, not exposed to external callers
from src.agent.teacher.problem_complexity import (
    ProblemComplexity,
    StructuralComplexity,
)

# Re-export ProblemComplexity so callers can subclass without knowing
# about the internal module
__all__ = ['StudentDifficultyEvaluator', 'ProblemComplexity']


class StudentDifficultyEvaluator:

    def __init__(
        self,
        max_actions:       int,
        penalty:           float             = 0.0,
        complexity_fn:     ProblemComplexity = None,
    ):
        self.max_actions   = max_actions
        self.penalty       = penalty
        self.complexity_fn = complexity_fn or StructuralComplexity(max_blocks=30)

        self._last_complexities: List[float] = []
        self._last_rewards:      List[float] = []

    def get_difficulty(
        self,
        problem_info_list: List[dict],
        nesig_problems:    Optional[list] = None,
    ) -> List[float]:
        rewards      = []
        complexities = []

        for i, info in enumerate(problem_info_list):
            num_goal_atoms = info.get('num_goal_atoms', 0)

            # Hard penalty for empty goals
            if num_goal_atoms == 0:
                rewards.append(-1.0)
                complexities.append(0.0)
                continue

            # Structural complexity — the only signal
            if nesig_problems is not None and i < len(nesig_problems):
                complexity = self.complexity_fn(nesig_problems[i])
            else:
                num_blocks = info.get('num_blocks', 1)
                complexity = min(num_goal_atoms / max(num_blocks, 1), 1.0)

            complexities.append(complexity)
            rewards.append(complexity * 100)

        self._last_complexities = complexities
        self._last_rewards      = rewards
        return rewards