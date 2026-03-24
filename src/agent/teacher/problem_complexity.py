"""
> problem_complexity.py

Standalone structural complexity measures for blocks world problems.

These functions operate on NeSIG problem objects and return a complexity
score in [0, 1] that reflects how hard a problem is to solve — independent
of any student performance.

The base class ProblemComplexity defines the interface. Subclass it to
implement alternative complexity measures without touching the evaluator.

Usage:
    from src.agent.teacher.problem_complexity import StructuralComplexity

    complexity_fn = StructuralComplexity()
    score = complexity_fn(nesig_problem)   # float in [0, 1]
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional


# ─────────────────────────────────────────────────────────────────────
# Base class — defines the interface
# ─────────────────────────────────────────────────────────────────────

class ProblemComplexity(ABC):
    """
    Abstract base class for problem complexity measures.

    Subclass this and implement __call__ to define a new complexity
    measure. The StudentDifficultyEvaluator accepts any subclass.
    """

    @abstractmethod
    def __call__(self, nesig_problem) -> float:
        """
        Compute the complexity of a NeSIG problem.

        Args:
            nesig_problem: a NeSIG PDDLProblem object with
                           initial_state and goal attributes.

        Returns:
            float in [0, 1] — 0 = trivial, 1 = maximally complex.
            Must return 0.0 for problems with empty goals.
        """
        raise NotImplementedError

    def batch(self, nesig_problems: list) -> list:
        """Convenience method — compute complexity for a list of problems."""
        return [self(p) for p in nesig_problems]


# ─────────────────────────────────────────────────────────────────────
# State parsing helpers (shared across implementations)
# ─────────────────────────────────────────────────────────────────────

def extract_support_map(pddl_state) -> Dict[int, Optional[int]]:
    """
    Extract a dict mapping each block index to what it is sitting on.

    Returns:
        support[i] = j    block i is on top of block j
        support[i] = -1   block i is on the table

    PDDLState stores atoms as:
        ('on',      (i, j))  → block i is on block j
        ('ontable', (i,))    → block i is on the table
    """
    support = {}
    for atom in pddl_state.atoms:
        name, args = atom
        if name == 'on':
            support[args[0]] = args[1]
        elif name == 'ontable':
            support[args[0]] = -1
    return support


def extract_goal_map(nesig_problem) -> Dict[int, Optional[int]]:
    goal_support = {}
    for atom in nesig_problem.goal:  
        name, args = atom
        if name == 'on':
            goal_support[args[0]] = args[1]
        elif name == 'ontable':
            goal_support[args[0]] = -1
    return goal_support


# ─────────────────────────────────────────────────────────────────────
# Structural complexity implementation
# ─────────────────────────────────────────────────────────────────────

class StructuralComplexity(ProblemComplexity):
    """
    Complexity based on three structural features, scaled by problem size.

    The raw structural score (misplacement, blockedness, goal density) is
    multiplied by a size factor:

        size_factor = n_blocks / max_blocks

    A score of 1.0 is only achievable on max-size problems that are also
    maximally hard structurally. A 5-block problem out of 30 is capped at
    5/30 ≈ 0.17 regardless of structural difficulty.

    Parameters
    ----------
    max_blocks : int
        Block count of the largest problem in the curriculum.
    w_misplacement : float  (default 0.4)
    w_blockedness  : float  (default 0.4)
    w_goal_density : float  (default 0.2)
    """

    def __init__(
        self,
        max_blocks:     int,
        w_misplacement: float = 0.4,
        w_blockedness:  float = 0.4,
        w_goal_density: float = 0.2,
    ):
        assert max_blocks > 0, "max_blocks must be a positive integer"
        assert abs(w_misplacement + w_blockedness + w_goal_density - 1.0) < 1e-6, \
            "Weights must sum to 1.0"
        self.max_blocks     = max_blocks
        self.w_misplacement = w_misplacement
        self.w_blockedness  = w_blockedness
        self.w_goal_density = w_goal_density

    def __call__(self, nesig_problem) -> float:
        """Compute size-scaled structural complexity in [0, 1]."""
        init_support = extract_support_map(nesig_problem.initial_state)
        goal_support = extract_goal_map(nesig_problem)
        num_blocks   = len(nesig_problem.initial_state.objects)

        if not goal_support:
            return 0.0

        m  = self._misplacement(init_support, goal_support)
        b  = self._blockedness(init_support, goal_support)
        gd = self._goal_density(goal_support, num_blocks)

        structural = (
            self.w_misplacement * m
            + self.w_blockedness  * b
            + self.w_goal_density * gd
        )

        # Larger problems can earn proportionally higher reward
        size_factor = min(num_blocks / self.max_blocks, 1.0)

        return structural * size_factor

    def _misplacement(self,
                      init_support: Dict[int, Optional[int]],
                      goal_support: Dict[int, Optional[int]]) -> float:
        misplaced = sum(
            1 for block, goal_pos in goal_support.items()
            if init_support.get(block) != goal_pos
        )
        return misplaced / len(goal_support)

    def _blockedness(self,
                     init_support: Dict[int, Optional[int]],
                     goal_support: Dict[int, Optional[int]]) -> float:
        misplaced = {
            block for block, goal_pos in goal_support.items()
            if init_support.get(block) != goal_pos
        }
        if not misplaced:
            return 0.0

        on_top_of = {
            support: block
            for block, support in init_support.items()
            if support != -1
        }

        blocked = sum(
            1 for block in misplaced
            if on_top_of.get(block) in misplaced
        )
        return blocked / len(misplaced)

    def _goal_density(self,
                      goal_support: Dict[int, Optional[int]],
                      num_blocks:   int) -> float:
        if num_blocks == 0:
            return 0.0
        return len(goal_support) / num_blocks