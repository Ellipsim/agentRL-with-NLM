"""
> test_problem_solver.py

Tests for the ProblemSolver class.
Tests solving problems with a random policy.
Runs on all .pddl files discovered in data/problems/

Note: RandomPolicy has very low success rate, so tests don't expect solutions.
Instead, they verify the solver runs correctly and collects valid trajectories.

Run with:
    pytest tests/test_problem_solver.py -v
    pytest -m solver -v
"""

import pytest
from copy import deepcopy

from src.agent.pddl.pddl_problem import PDDLProblem
from src.agent.learning.generative_policy import RandomPolicy
from src.agent.pddl.problem_solver import ProblemSolver

@pytest.mark.solver_random
class TestSolverRandomPolicy:
    """Tests for ProblemSolver with RandomPolicy."""

    @pytest.fixture
    def solver(self, parser):
        """Create a ProblemSolver with RandomPolicy."""
        policy = RandomPolicy()
        return ProblemSolver(parser, policy)

    def test_solver_initializes(self, parser):
        """Test that ProblemSolver initializes correctly."""
        policy = RandomPolicy()
        solver = ProblemSolver(parser, policy)
        assert solver is not None
        assert solver.parser is not None
        assert solver.policy is not None

    def test_solve_single_problem_returns_results(self, solver, parser, problem_file):
        """Test that solving a single problem returns valid results."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=50)
        
        is_solved, info, trajectories, elapsed = solver.solve_problems(
            [problem], list_max_actions=50
        )
        
        assert len(is_solved) == 1
        assert isinstance(is_solved[0], bool)
        assert len(info) == 1
        assert len(trajectories) == 1
        assert elapsed >= 0
        # RandomPolicy might not solve, but should produce at least one step
        assert len(trajectories[0]) > 0

    def test_solve_returns_correct_number_of_results(self, solver, fresh_parser, problem_file):
        """Test that solving multiple problems returns correct number of results."""
        problem1 = PDDLProblem.load_from_pddl(fresh_parser(), problem_file, max_actions=50)
        problem2 = PDDLProblem.load_from_pddl(fresh_parser(), problem_file, max_actions=50)
        problems = [problem1, problem2]
        
        is_solved, info, trajectories, _ = solver.solve_problems(problems, list_max_actions=50)
        
        assert len(is_solved) == 2
        assert len(info) == 2
        assert len(trajectories) == 2

    def test_solve_resets_problems_before_solving(self, solver, parser, problem_file):
        """Test that solve_problems resets each problem (idempotent)."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=50)
        
        # Solve once
        is_solved1, _, trajectories1, _ = solver.solve_problems([problem], list_max_actions=50)
        first_step_atoms1 = trajectories1[0][0]['state'].atoms
        
        # Solve again on the same problem
        is_solved2, _, trajectories2, _ = solver.solve_problems([problem], list_max_actions=50)
        first_step_atoms2 = trajectories2[0][0]['state'].atoms
        
        # Both runs should start from the same initial state
        assert first_step_atoms1 == first_step_atoms2

    def test_trajectory_steps_have_required_keys(self, solver, parser, problem_file):
        """Test that trajectory steps have all required keys."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=50)
        _, _, trajectories, _ = solver.solve_problems([problem], list_max_actions=50)
        
        required_keys = {
            'state', 'internal_state', 'applicable_actions',
            'chosen_action', 'chosen_action_ind', 'action_log_prob', 'reward',
        }
        
        for step in trajectories[0]:
            assert required_keys.issubset(step.keys()), \
                f"Step missing keys: {required_keys - step.keys()}"

    def test_chosen_action_is_in_applicable_actions(self, solver, parser, problem_file):
        """Test that chosen action is always in the applicable actions."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=50)
        _, _, trajectories, _ = solver.solve_problems([problem], list_max_actions=50)
        
        for step in trajectories[0]:
            assert step['chosen_action'] in step['applicable_actions'], \
                "Chosen action must be in applicable actions"

    def test_chosen_action_ind_matches_chosen_action(self, solver, parser, problem_file):
        """Test that chosen_action_ind correctly indexes into applicable_actions."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=50)
        _, _, trajectories, _ = solver.solve_problems([problem], list_max_actions=50)
        
        for step in trajectories[0]:
            action = step['chosen_action']
            ind = step['chosen_action_ind']
            assert step['applicable_actions'][ind] == action

    def test_trajectory_length_respects_budget(self, solver, parser, problem_file):
        """Test that trajectory length respects the max_actions budget."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
        max_actions = 10
        
        _, _, trajectories, _ = solver.solve_problems([problem], list_max_actions=max_actions)
        
        # Trajectory should not exceed budget
        assert len(trajectories[0]) <= max_actions
        # But should have at least 1 step (goal might be reached or budget hit)
        assert len(trajectories[0]) >= 1

    def test_budget_exhaustion_terminates_correctly(self, solver, parser, problem_file):
        """Test that trajectory terminates when budget is exhausted."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=5)
        _, info, trajectories, _ = solver.solve_problems([problem], list_max_actions=5)
        
        # With such a small budget, most trajectories will hit the budget limit
        # (goal is unlikely to be reached with only 5 actions)
        assert info[0]['num_steps'] <= 5

    def test_broadcast_max_actions_to_all_problems(self, solver, fresh_parser, problem_file):
        """Test that scalar max_actions broadcasts to all problems."""
        problem1 = PDDLProblem.load_from_pddl(fresh_parser(), problem_file, max_actions=100)
        problem2 = PDDLProblem.load_from_pddl(fresh_parser(), problem_file, max_actions=100)
        problems = [problem1, problem2]
        
        _, info, _, _ = solver.solve_problems(problems, list_max_actions=15)
        
        assert info[0]['max_actions'] == 15
        assert info[1]['max_actions'] == 15

    def test_per_problem_max_actions(self, solver, fresh_parser, problem_file):
        """Test that per-problem max_actions are respected."""
        problem1 = PDDLProblem.load_from_pddl(fresh_parser(), problem_file, max_actions=100)
        problem2 = PDDLProblem.load_from_pddl(fresh_parser(), problem_file, max_actions=100)
        problems = [problem1, problem2]
        
        _, info, _, _ = solver.solve_problems(problems, list_max_actions=[10, 20])
        
        assert info[0]['max_actions'] == 10
        assert info[1]['max_actions'] == 20
        # Num steps should not exceed their respective budgets
        assert info[0]['num_steps'] <= 10
        assert info[1]['num_steps'] <= 20

    def test_info_dict_has_required_keys(self, solver, parser, problem_file):
        """Test that info dict has all required keys."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=50)
        _, info, _, _ = solver.solve_problems([problem], list_max_actions=50)
        
        required = {
            'num_steps', 'max_actions', 'goal_reached', 'action_history',
            'num_objects', 'num_goal_atoms'
        }
        assert required.issubset(info[0].keys())

    def test_info_num_steps_matches_trajectory_length(self, solver, parser, problem_file):
        """Test that info['num_steps'] matches trajectory length."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=50)
        _, info, trajectories, _ = solver.solve_problems([problem], list_max_actions=50)
        
        assert info[0]['num_steps'] == len(trajectories[0])

    def test_info_action_history_matches_trajectory_actions(self, solver, parser, problem_file):
        """Test that info['action_history'] matches chosen actions in trajectory."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=50)
        _, info, trajectories, _ = solver.solve_problems([problem], list_max_actions=50)
        
        traj_actions = [step['chosen_action'] for step in trajectories[0]]
        assert info[0]['action_history'] == traj_actions

    def test_info_num_goal_atoms(self, solver, parser, problem_file):
        """Test that info['num_goal_atoms'] is correct."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=50)
        _, info, _, _ = solver.solve_problems([problem], list_max_actions=50)
        
        expected_goal_atoms = len(problem.goal) if problem.goal else 0
        assert info[0]['num_goal_atoms'] == expected_goal_atoms

    def test_goal_reached_flag_correct(self, solver, parser, problem_file):
        """Test that goal_reached flag matches is_solved."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=50)
        is_solved, info, _, _ = solver.solve_problems([problem], list_max_actions=50)
        
        assert info[0]['goal_reached'] == is_solved[0]

    def test_elapsed_time_positive(self, solver, parser, problem_file):
        """Test that elapsed time is measured."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=50)
        _, _, _, elapsed = solver.solve_problems([problem], list_max_actions=50)
        
        assert elapsed >= 0

    def test_solve_batch_of_same_problem(self, solver, fresh_parser, problem_file):
        """Test solving multiple independent copies of the same problem."""
        problems = [
            PDDLProblem.load_from_pddl(fresh_parser(), problem_file, max_actions=50)
            for _ in range(3)
        ]
        
        is_solved, info, trajectories, _ = solver.solve_problems(problems, list_max_actions=50)
        
        assert len(is_solved) == 3
        # Each problem should have at least one step (all have applicable actions)
        assert all(len(t) > 0 for t in trajectories)

    def test_action_log_prob_is_set(self, solver, parser, problem_file):
        """Test that action_log_prob is set for each step."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=50)
        _, _, trajectories, _ = solver.solve_problems([problem], list_max_actions=50)
        
        for step in trajectories[0]:
            assert step['action_log_prob'] is not None

    def test_state_snapshots_are_independent(self, solver, parser, problem_file):
        """Test that state snapshots in trajectory are independent copies."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=50)
        _, _, trajectories, _ = solver.solve_problems([problem], list_max_actions=50)
        
        # Each state should be a snapshot of that moment
        # (modifying one shouldn't affect others)
        if len(trajectories[0]) > 1:
            step0_state = trajectories[0][0]['state']
            step1_state = trajectories[0][1]['state']
            # They should be different (action was applied between them)
            assert step0_state.atoms != step1_state.atoms or \
                   len(trajectories[0]) == 1  # Or only 1 step if goal reached

    def test_applicable_actions_not_empty(self, solver, parser, problem_file):
        """Test that every step has applicable actions to choose from."""
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=50)
        _, _, trajectories, _ = solver.solve_problems([problem], list_max_actions=50)
        
        for step in trajectories[0]:
            assert len(step['applicable_actions']) > 0, \
                "Each step should have at least one applicable action"
            
    # # Parece un bug de lifted_pddl
    # def test_parser_reader_internals(self, parser, problem_file):
    #     """Check the _reader.problem and _reader.parser for FOL language state."""
    #     from copy import deepcopy
        
    #     print("\n=== Before any load ===")
    #     print(f"parser._reader.problem: {parser._reader.problem}")
        
    #     # Create deepcopy
    #     parser_copy = deepcopy(parser)

    #     # Load problem once
    #     problem1 = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=50)
        
    #     print("\n=== After first load ===")
    #     print(f"parser._reader.problem id: {id(parser._reader.problem)}")
    #     lang = parser._reader.problem.language
    #     print(f"language id: {id(lang)}")
    #     print(f"language.constants: {list(lang.constants())[:5]}")  # Try as method
        
  
    #     print("\n=== Deepcopy ===")
    #     print(f"parser_copy._reader.problem id: {id(parser_copy._reader.problem)}")
    #     print(f"Same problem object? {id(parser._reader.problem) == id(parser_copy._reader.problem)}")
        
    #     lang_copy = parser_copy._reader.problem.language
    #     print(f"language_copy id: {id(lang_copy)}")
    #     print(f"Same language object? {id(lang) == id(lang_copy)}")
    #     print(f"language_copy.constants: {list(lang_copy.constants())[:5]}")