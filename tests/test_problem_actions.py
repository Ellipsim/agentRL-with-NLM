"""
> test_problem_actions.py

Tests for applicable actions.
Runs on all .pddl files discovered in data/problems/

Run with:
    pytest tests/test_problem_actions.py -v
    pytest -m actions -v
"""

import pytest
from src.agent.pddl.pddl_problem import PDDLProblem


@pytest.mark.actions
class TestProblemActions:
    """Tests for applicable actions."""

    def test_problem_has_applicable_actions(self, parser, problem_file):
        """Test that each problem has applicable actions in the initial state."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        actions = problem.applicable_ground_actions()
        assert len(actions) > 0, f"Problem {problem_file.stem} has no applicable actions"

    def test_applicable_ground_actions_returns_tuple(self, parser, problem_file):
        """Applicable ground actions should return a tuple."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        actions = problem.applicable_ground_actions()
        assert isinstance(actions, tuple)

    def test_applicable_ground_actions_are_valid_format(self, parser, problem_file):
        """Applicable ground actions should have correct format."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        for action in problem.applicable_ground_actions():
            name, params = action
            assert isinstance(name, str)
            assert isinstance(params, tuple)

    def test_no_repeated_object_indices_in_actions(self, parser, problem_file):
        """Actions should not have repeated object indices."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        for name, params in problem.applicable_ground_actions():
            assert len(params) == len(set(params)), \
                f"Action {name}{params} has repeated object indices"

    def test_is_ground_action_applicable_true_for_applicable(self, parser, problem_file):
        """All returned applicable actions must pass applicability check."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        actions = problem.applicable_ground_actions()
        for action in actions:
            assert problem.is_ground_action_applicable(action)