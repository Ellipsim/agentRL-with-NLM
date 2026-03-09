"""
> test_problem_solving.py

Tests for action execution, reset functionality, and deep copy independence.
Runs on all .pddl files discovered in data/problems/

Run with:
    pytest tests/test_problem_solving.py -v
    pytest -m solving -v
"""

import pytest
from copy import deepcopy
from src.agent.pddl.pddl_problem import PDDLProblem


@pytest.mark.solving
class TestActionExecution:
    """Tests for action execution and state transitions."""

    def test_apply_action_increments_counter(self, parser, problem_file):
        """Applying an action should increment the counter."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        action = problem.applicable_ground_actions()[0]
        problem.apply_action(action)
        assert problem.num_actions_executed == 1

    def test_apply_action_appends_to_history(self, parser, problem_file):
        """Applying an action should append to history."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        action = problem.applicable_ground_actions()[0]
        problem.apply_action(action)
        assert problem.action_history == [action]

    def test_apply_action_changes_current_state(self, parser, problem_file):
        """Applying an action should change the current state."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        atoms_before = problem.current_state.atoms
        action = problem.applicable_ground_actions()[0]
        problem.apply_action(action)
        assert problem.current_state.atoms != atoms_before

    def test_apply_action_does_not_change_initial_state(self, parser, problem_file):
        """Applying actions should not change the initial state."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        initial_atoms = problem.initial_state.atoms
        for _ in range(min(3, len(problem.applicable_ground_actions()))):
            actions = problem.applicable_ground_actions()
            if actions:
                problem.apply_action(actions[0])
        assert problem.initial_state.atoms == initial_atoms

    def test_perc_actions_executed_updates(self, parser, problem_file):
        """Percentage of actions executed should update correctly."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=20)
        action = problem.applicable_ground_actions()[0]
        problem.apply_action(action)
        assert problem.perc_actions_executed == pytest.approx(1 / 20)

    def test_budget_exhaustion_raises(self, parser, problem_file):
        """Should raise error when budget is exhausted."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=1)
        action = problem.applicable_ground_actions()[0]
        problem.apply_action(action)
        # Second action should raise
        actions = problem.applicable_ground_actions()
        if actions:
            with pytest.raises(ValueError, match="budget"):
                problem.apply_action(actions[0])


@pytest.mark.solving
class TestReset:
    """Tests for resetting problem state."""

    def test_reset_restores_current_state(self, parser, problem_file):
        """Reset should restore the current state."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        initial_atoms = problem.initial_state.atoms
        problem.apply_action(problem.applicable_ground_actions()[0])
        assert problem.current_state.atoms != initial_atoms
        problem.reset()
        assert problem.current_state.atoms == initial_atoms

    def test_reset_clears_action_history(self, parser, problem_file):
        """Reset should clear the action history."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        problem.apply_action(problem.applicable_ground_actions()[0])
        problem.reset()
        assert problem.action_history == []
        assert problem.num_actions_executed == 0

    def test_reset_does_not_change_goal(self, parser, problem_file):
        """Reset should not change the goal."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        goal_before = problem.goal
        problem.apply_action(problem.applicable_ground_actions()[0])
        problem.reset()
        assert problem.goal == goal_before


@pytest.mark.solving
class TestDeepCopy:
    """Tests for deep copy independence."""

    def test_deepcopy_is_independent(self, parser, problem_file):
        """Deepcopy should create an independent copy."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        copy = deepcopy(problem)
        copy.apply_action(copy.applicable_ground_actions()[0])
        # Original must be untouched
        assert problem.num_actions_executed == 0
        assert problem.current_state.atoms == problem.initial_state.atoms

    def test_deepcopy_preserves_goal(self, parser, problem_file):
        """Deepcopy should preserve the goal."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        copy = deepcopy(problem)
        assert copy.goal == problem.goal