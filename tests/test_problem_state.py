"""
> test_problem_state.py

Tests for problem state and state properties.
Runs on all .pddl files discovered in data/problems/

Run with:
    pytest tests/test_problem_state.py -v
    pytest -m state -v
"""

import pytest
from src.agent.pddl.pddl_problem import PDDLProblem


@pytest.mark.state
class TestProblemState:
    """Tests for problem state and state properties."""

    def test_current_state_equals_initial_state_at_start(self, parser, problem_file):
        """Current state should equal initial state at the start."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        assert problem.current_state.atoms == problem.initial_state.atoms

    def test_num_actions_executed_starts_at_zero(self, parser, problem_file):
        """Number of actions executed should start at zero."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        assert problem.num_actions_executed == 0

    def test_action_history_starts_empty(self, parser, problem_file):
        """Action history should start empty."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        assert problem.action_history == []

    def test_max_actions_set(self, parser, problem_file):
        """Max actions should be set correctly."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        assert problem.max_actions == 100

    def test_perc_actions_executed_starts_at_zero(self, parser, problem_file):
        """Percentage of actions executed should start at zero."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        assert problem.perc_actions_executed == 0.0

    def test_state_num_objects_matches_problem(self, parser, problem_file):
        """State number of objects should match problem."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        state = problem.current_state
        assert state.num_objects == problem.initial_state.num_objects

    def test_state_atoms_are_a_set(self, parser, problem_file):
        """State atoms should be a set."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        assert isinstance(problem.current_state.atoms, set)

    def test_num_atoms_each_type_sums_to_total(self, parser, problem_file):
        """Sum of atoms each type should equal total atoms."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        state = problem.current_state
        assert sum(state.num_atoms_each_type) == state.num_atoms

    def test_num_objects_each_type_sums_to_total(self, parser, problem_file):
        """Sum of objects each type should equal total objects."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        state = problem.current_state
        assert sum(state.num_objects_each_type) == state.num_objects