"""
> test_problem_loading.py

Tests for loading problems and basic structure.
Runs on all .pddl files discovered in data/problems/

Run with:
    pytest tests/test_problem_loading.py -v
    pytest -m loading -v
"""

import pytest
from src.agent.pddl.pddl_problem import PDDLProblem


@pytest.mark.loading
class TestProblemLoading:
    """Tests for loading problems and basic structure."""

    def test_problem_loads(self, parser, problem_file):
        """Test that each problem file loads correctly."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        assert problem is not None
        assert problem.initial_state.num_objects > 0

    def test_problem_has_goal(self, parser, problem_file):
        """Test that each problem has a goal."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        assert problem.goal is not None
        assert len(problem.goal) > 0

    def test_problem_has_initial_state(self, parser, problem_file):
        """Test that each problem has an initial state."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        assert problem.initial_state.num_atoms > 0