# """
# > test_compendium.py

# Unit and integration tests for the symbolic solving layer.
# Tests automatically discover and run on ALL .pddl files in data/problems/

# Run with:
#     pytest tests/test_compendium.py -v

# Requirements:
#     - lifted_pddl must be installed and importable
#     - PDDL files must be in data/domains and data/problems/
# """

# import pytest
# from pathlib import Path
# from copy import deepcopy
# from lifted_pddl import Parser

# from agent.pddl.pddl_problem import PDDLProblem
# from agent.pddl.pddl_state import PDDLState


# # ===========================================================================
# # PDDL fixtures — load from data/ directory
# # ===========================================================================

# @pytest.fixture(scope="session")
# def data_dir():
#     """Return path to the data directory."""
#     return Path(__file__).parent.parent / "data"


# @pytest.fixture(scope="session")
# def domain_file(data_dir):
#     """Return path to the blocksworld domain."""
#     return data_dir / "domains" / "blocksworld.pddl"


# @pytest.fixture
# def parser(domain_file):
#     """A Parser already loaded with the blocksworld domain."""
#     p = Parser()
#     p.parse_domain(str(domain_file))
#     return p


# @pytest.fixture(params=[])
# def problem_file(request):
#     """
#     Parametrized fixture that automatically loads ALL .pddl files from data/problems/.
#     Each test using this fixture will run once for each problem file found.
#     """
#     return request.param


# def pytest_generate_tests(metafunc):
#     """Automatically parametrize tests that use problem_file fixture."""
#     if "problem_file" in metafunc.fixturenames:
#         data_dir = Path(__file__).parent.parent / "data"
#         problems_dir = data_dir / "problems"
#         problem_files = sorted(problems_dir.glob("**/*.pddl"))  # Recursive glob
        
#         if not problem_files:
#             pytest.skip(f"No .pddl files found in {problems_dir}")
        
#         metafunc.parametrize(
#             "problem_file",
#             problem_files,
#             ids=[f.stem for f in problem_files]  # Use problem names as test IDs
#         )


# # ===========================================================================
# # Tests that run on ALL problems in data/problems/
# # ===========================================================================

# class TestAllProblems:
#     """Run basic checks on ALL problems in the problems folder."""

#     def test_problem_loads(self, parser, problem_file):
#         """Test that each problem file loads correctly."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         assert problem is not None
#         assert problem.initial_state.num_objects > 0

#     def test_problem_has_goal(self, parser, problem_file):
#         """Test that each problem has a goal."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         assert problem.goal is not None
#         assert len(problem.goal) > 0

#     def test_problem_has_initial_state(self, parser, problem_file):
#         """Test that each problem has an initial state."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         assert problem.initial_state.num_atoms > 0

#     def test_problem_has_applicable_actions(self, parser, problem_file):
#         """Test that each problem has applicable actions in the initial state."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         actions = problem.applicable_ground_actions()
#         assert len(actions) > 0, f"Problem {problem_file.stem} has no applicable actions"

#     def test_current_state_equals_initial_state_at_start(self, parser, problem_file):
#         """Current state should equal initial state at the start."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         assert problem.current_state.atoms == problem.initial_state.atoms

#     def test_num_actions_executed_starts_at_zero(self, parser, problem_file):
#         """Number of actions executed should start at zero."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         assert problem.num_actions_executed == 0

#     def test_action_history_starts_empty(self, parser, problem_file):
#         """Action history should start empty."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         assert problem.action_history == []

#     def test_goal_not_reached_at_start(self, parser, problem_file):
#         """Goal should not be reached at the start (unless trivial problem)."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         # Only check if goal is not already satisfied (some problems might have trivial goals)
#         if len(problem.goal) > 0:
#             # If there are goal atoms, at least one should not be satisfied initially
#             goal_atoms = set(problem.goal)
#             if not goal_atoms.issubset(problem.current_state.atoms):
#                 assert not problem.is_goal_reached()

#     def test_max_actions_set(self, parser, problem_file):
#         """Max actions should be set correctly."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         assert problem.max_actions == 100

#     def test_perc_actions_executed_starts_at_zero(self, parser, problem_file):
#         """Percentage of actions executed should start at zero."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         assert problem.perc_actions_executed == 0.0

#     def test_applicable_ground_actions_returns_tuple(self, parser, problem_file):
#         """Applicable ground actions should return a tuple."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         actions = problem.applicable_ground_actions()
#         assert isinstance(actions, tuple)

#     def test_applicable_ground_actions_are_valid_format(self, parser, problem_file):
#         """Applicable ground actions should have correct format."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         for action in problem.applicable_ground_actions():
#             name, params = action
#             assert isinstance(name, str)
#             assert isinstance(params, tuple)

#     def test_no_repeated_object_indices_in_actions(self, parser, problem_file):
#         """Actions should not have repeated object indices."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         for name, params in problem.applicable_ground_actions():
#             assert len(params) == len(set(params)), \
#                 f"Action {name}{params} has repeated object indices"

#     def test_is_ground_action_applicable_true_for_applicable(self, parser, problem_file):
#         """All returned applicable actions must pass applicability check."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         actions = problem.applicable_ground_actions()
#         for action in actions:
#             assert problem.is_ground_action_applicable(action)

#     def test_apply_action_increments_counter(self, parser, problem_file):
#         """Applying an action should increment the counter."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         action = problem.applicable_ground_actions()[0]
#         problem.apply_action(action)
#         assert problem.num_actions_executed == 1

#     def test_apply_action_appends_to_history(self, parser, problem_file):
#         """Applying an action should append to history."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         action = problem.applicable_ground_actions()[0]
#         problem.apply_action(action)
#         assert problem.action_history == [action]

#     def test_apply_action_changes_current_state(self, parser, problem_file):
#         """Applying an action should change the current state."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         atoms_before = problem.current_state.atoms
#         action = problem.applicable_ground_actions()[0]
#         problem.apply_action(action)
#         assert problem.current_state.atoms != atoms_before

#     def test_apply_action_does_not_change_initial_state(self, parser, problem_file):
#         """Applying actions should not change the initial state."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         initial_atoms = problem.initial_state.atoms
#         for _ in range(min(3, len(problem.applicable_ground_actions()))):
#             actions = problem.applicable_ground_actions()
#             if actions:
#                 problem.apply_action(actions[0])
#         assert problem.initial_state.atoms == initial_atoms

#     def test_perc_actions_executed_updates(self, parser, problem_file):
#         """Percentage of actions executed should update correctly."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=20)
#         action = problem.applicable_ground_actions()[0]
#         problem.apply_action(action)
#         assert problem.perc_actions_executed == pytest.approx(1 / 20)

#     def test_budget_exhaustion_raises(self, parser, problem_file):
#         """Should raise error when budget is exhausted."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=1)
#         action = problem.applicable_ground_actions()[0]
#         problem.apply_action(action)
#         # Second action should raise
#         actions = problem.applicable_ground_actions()
#         if actions:
#             with pytest.raises(ValueError, match="budget"):
#                 problem.apply_action(actions[0])

#     def test_reset_restores_current_state(self, parser, problem_file):
#         """Reset should restore the current state."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         initial_atoms = problem.initial_state.atoms
#         problem.apply_action(problem.applicable_ground_actions()[0])
#         assert problem.current_state.atoms != initial_atoms
#         problem.reset()
#         assert problem.current_state.atoms == initial_atoms

#     def test_reset_clears_action_history(self, parser, problem_file):
#         """Reset should clear the action history."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         problem.apply_action(problem.applicable_ground_actions()[0])
#         problem.reset()
#         assert problem.action_history == []
#         assert problem.num_actions_executed == 0

#     def test_reset_does_not_change_goal(self, parser, problem_file):
#         """Reset should not change the goal."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         goal_before = problem.goal
#         problem.apply_action(problem.applicable_ground_actions()[0])
#         problem.reset()
#         assert problem.goal == goal_before

#     def test_deepcopy_is_independent(self, parser, problem_file):
#         """Deepcopy should create an independent copy."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         copy = deepcopy(problem)
#         copy.apply_action(copy.applicable_ground_actions()[0])
#         # Original must be untouched
#         assert problem.num_actions_executed == 0
#         assert problem.current_state.atoms == problem.initial_state.atoms

#     def test_deepcopy_preserves_goal(self, parser, problem_file):
#         """Deepcopy should preserve the goal."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         copy = deepcopy(problem)
#         assert copy.goal == problem.goal

#     def test_state_num_objects_matches_problem(self, parser, problem_file):
#         """State number of objects should match problem."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         state = problem.current_state
#         assert state.num_objects == problem.initial_state.num_objects

#     def test_state_atoms_are_a_set(self, parser, problem_file):
#         """State atoms should be a set."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         assert isinstance(problem.current_state.atoms, set)

#     def test_num_atoms_each_type_sums_to_total(self, parser, problem_file):
#         """Sum of atoms each type should equal total atoms."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         state = problem.current_state
#         assert sum(state.num_atoms_each_type) == state.num_atoms

#     def test_num_objects_each_type_sums_to_total(self, parser, problem_file):
#         """Sum of objects each type should equal total objects."""
#         problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=100)
#         state = problem.current_state
#         assert sum(state.num_objects_each_type) == state.num_objects