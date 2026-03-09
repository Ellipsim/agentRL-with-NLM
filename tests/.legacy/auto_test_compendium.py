# """
# > test_solver.py

# Unit and integration tests for the symbolic solving layer.
# Tests are fully independent of any neural policy — they use RandomPolicy
# (which requires no training) or a scripted deterministic policy.

# Run with:
#     pytest tests/test_solver.py -v

# Requirements:
#     - lifted_pddl must be installed and importable
#     - The test creates temporary PDDL files in a tmp directory (handled by pytest fixtures)
# """

# import pytest
# import tempfile
# import os
# from pathlib import Path
# from copy import deepcopy
# from lifted_pddl import Parser

# from agent.pddl.pddl_problem import PDDLProblem
# from agent.pddl.pddl_state import PDDLState
# from src.agent.learning.generative_policy import RandomPolicy
# from src.agent.pddl.problem_solver import ProblemSolver


# # ===========================================================================
# # PDDL fixtures — minimal blocksworld domain and two problems
# # ===========================================================================

# BLOCKSWORLD_DOMAIN = """
# (define (domain blocksworld)
#   (:requirements :strips :typing)
#   (:types block)
#   (:predicates
#     (on ?x - block ?y - block)
#     (ontable ?x - block)
#     (clear ?x - block)
#     (handempty)
#     (holding ?x - block))

#   (:action pick-up
#     :parameters (?x - block)
#     :precondition (and (clear ?x) (ontable ?x) (handempty))
#     :effect (and (not (ontable ?x)) (not (clear ?x)) (not (handempty))
#                  (holding ?x)))

#   (:action put-down
#     :parameters (?x - block)
#     :precondition (holding ?x)
#     :effect (and (not (holding ?x)) (clear ?x) (handempty) (ontable ?x)))

#   (:action stack
#     :parameters (?x - block ?y - block)
#     :precondition (and (holding ?x) (clear ?y))
#     :effect (and (not (holding ?x)) (not (clear ?y))
#                  (clear ?x) (handempty) (on ?x ?y)))

#   (:action unstack
#     :parameters (?x - block ?y - block)
#     :precondition (and (on ?x ?y) (clear ?x) (handempty))
#     :effect (and (holding ?x) (clear ?y) (not (clear ?x))
#                  (not (handempty)) (not (on ?x ?y)))))
# """.strip()

# # Problem: A is on B, both on table.  Goal: B on top of A.
# # Optimal solution: unstack A B → put-down A → pick-up B → stack B A  (4 steps)
# BLOCKSWORLD_PROBLEM_SIMPLE = """
# (define (problem bw-simple)
#   (:domain blocksworld)
#   (:objects obj0 obj1 - block)
#   (:init
#     (ontable obj1)
#     (on obj0 obj1)
#     (clear obj0)
#     (handempty))
#   (:goal (and
#     (on obj1 obj0))))
# """.strip()

# # Problem: three blocks, all on table.  Goal: tower A on B on C.
# BLOCKSWORLD_PROBLEM_TOWER = """
# (define (problem bw-tower)
#   (:domain blocksworld)
#   (:objects obj0 obj1 obj2 - block)
#   (:init
#     (ontable obj0)
#     (ontable obj1)
#     (ontable obj2)
#     (clear obj0)
#     (clear obj1)
#     (clear obj2)
#     (handempty))
#   (:goal (and
#     (on obj0 obj1)
#     (on obj1 obj2))))
# """.strip()


# @pytest.fixture(scope="module")
# def pddl_files(tmp_path_factory):
#     """Write domain and problem PDDL strings to temp files, return their paths."""
#     tmp = tmp_path_factory.mktemp("pddl")

#     domain_path = tmp / "domain.pddl"
#     domain_path.write_text(BLOCKSWORLD_DOMAIN)

#     simple_path = tmp / "simple.pddl"
#     simple_path.write_text(BLOCKSWORLD_PROBLEM_SIMPLE)

#     tower_path = tmp / "tower.pddl"
#     tower_path.write_text(BLOCKSWORLD_PROBLEM_TOWER)

#     return {"domain": domain_path, "simple": simple_path, "tower": tower_path}


# @pytest.fixture
# def parser(pddl_files):
#     """A Parser already loaded with the blocksworld domain."""
#     p = Parser()
#     p.parse_domain(str(pddl_files["domain"]))
#     return p


# @pytest.fixture
# def simple_problem(parser, pddl_files):
#     """Fresh PDDLProblemSolver for the simple 2-block problem."""
#     return PDDLProblem.load_from_pddl(parser, pddl_files["simple"], max_actions=20)


# @pytest.fixture
# def tower_problem(parser, pddl_files):
#     """Fresh PDDLProblemSolver for the 3-block tower problem."""
#     return PDDLProblem.load_from_pddl(parser, pddl_files["tower"], max_actions=20)


# # ===========================================================================
# # 1. PDDLProblemSolver — construction and properties
# # ===========================================================================

# class TestPDDLProblemSolverConstruction:

#     def test_load_from_pddl_creates_problem(self, simple_problem):
#         assert simple_problem is not None

#     def test_initial_state_has_objects(self, simple_problem):
#         assert simple_problem.initial_state.num_objects == 2

#     def test_initial_state_has_atoms(self, simple_problem):
#         # on, ontable x2, clear, handempty → 5 atoms
#         assert simple_problem.initial_state.num_atoms == 4

#     def test_goal_is_not_empty(self, simple_problem):
#         assert simple_problem.goal is not None
#         assert len(simple_problem.goal) > 0

#     def test_goal_contains_on_atom(self, simple_problem):
#         pred_names = [a[0] for a in simple_problem.goal]
#         assert 'on' in pred_names

#     def test_current_state_equals_initial_state_at_start(self, simple_problem):
#         assert simple_problem.current_state.atoms == simple_problem.initial_state.atoms

#     def test_num_actions_executed_starts_at_zero(self, simple_problem):
#         assert simple_problem.num_actions_executed == 0

#     def test_action_history_starts_empty(self, simple_problem):
#         assert simple_problem.action_history == []

#     def test_goal_not_reached_at_start(self, simple_problem):
#         # The initial state does not satisfy the goal (A on B, goal is B on A)
#         assert not simple_problem.is_goal_reached()

#     def test_max_actions_set(self, simple_problem):
#         assert simple_problem.max_actions == 20

#     def test_perc_actions_executed_starts_at_zero(self, simple_problem):
#         assert simple_problem.perc_actions_executed == 0.0


# # ===========================================================================
# # 2. PDDLProblemSolver — applicable actions
# # ===========================================================================

# class TestApplicableActions:

#     def test_applicable_ground_actions_returns_tuple(self, simple_problem):
#         actions = simple_problem.applicable_ground_actions()
#         assert isinstance(actions, tuple)

#     def test_applicable_ground_actions_nonempty(self, simple_problem):
#         actions = simple_problem.applicable_ground_actions()
#         assert len(actions) > 0

#     def test_applicable_ground_actions_are_tuples(self, simple_problem):
#         for action in simple_problem.applicable_ground_actions():
#             name, params = action
#             assert isinstance(name, str)
#             assert isinstance(params, tuple)

#     def test_no_repeated_object_indices_in_actions(self, simple_problem):
#         for name, params in simple_problem.applicable_ground_actions():
#             assert len(params) == len(set(params)), \
#                 f"Action {name}{params} has repeated object indices"

#     def test_applicable_lifted_actions_are_subset_of_domain(self, simple_problem):
#         domain_action_names = {a[0] for a in simple_problem.parser.actions}
#         lifted = simple_problem.applicable_lifted_actions()
#         assert all(name in domain_action_names for name in lifted)

#     def test_is_ground_action_applicable_true_for_applicable(self, simple_problem):
#         actions = simple_problem.applicable_ground_actions()
#         # Every action returned by applicable_ground_actions must pass the check
#         for action in actions:
#             assert simple_problem.is_ground_action_applicable(action)

#     def test_initial_state_allows_unstack(self, simple_problem):
#         # obj0 is on obj1 and clear → unstack(obj0, obj1) should be applicable
#         lifted = simple_problem.applicable_lifted_actions()
#         assert 'unstack' in lifted

#     def test_pick_up_not_applicable_when_holding(self, simple_problem):
#         # Force a 'holding' state by applying unstack
#         problem = deepcopy(simple_problem)
#         actions = problem.applicable_ground_actions()
#         unstack_actions = [a for a in actions if a[0] == 'unstack']
#         assert unstack_actions, "Expected unstack to be applicable in initial state"
#         problem.apply_action(unstack_actions[0])
#         # Now holding a block → pick-up should NOT be applicable
#         lifted_after = problem.applicable_lifted_actions()
#         assert 'pick-up' not in lifted_after


# # ===========================================================================
# # 3. PDDLProblemSolver — apply_action and state transitions
# # ===========================================================================

# class TestApplyAction:

#     def test_apply_action_increments_counter(self, simple_problem):
#         problem = deepcopy(simple_problem)
#         action = problem.applicable_ground_actions()[0]
#         problem.apply_action(action)
#         assert problem.num_actions_executed == 1

#     def test_apply_action_appends_to_history(self, simple_problem):
#         problem = deepcopy(simple_problem)
#         action = problem.applicable_ground_actions()[0]
#         problem.apply_action(action)
#         assert problem.action_history == [action]

#     def test_apply_action_changes_current_state(self, simple_problem):
#         problem = deepcopy(simple_problem)
#         atoms_before = problem.current_state.atoms
#         action = problem.applicable_ground_actions()[0]
#         problem.apply_action(action)
#         assert problem.current_state.atoms != atoms_before

#     def test_apply_action_does_not_change_initial_state(self, simple_problem):
#         problem = deepcopy(simple_problem)
#         initial_atoms = problem.initial_state.atoms
#         for _ in range(3):
#             actions = problem.applicable_ground_actions()
#             if actions:
#                 problem.apply_action(actions[0])
#         assert problem.initial_state.atoms == initial_atoms

#     def test_perc_actions_executed_updates(self, simple_problem):
#         problem = deepcopy(simple_problem)
#         action = problem.applicable_ground_actions()[0]
#         problem.apply_action(action)
#         assert problem.perc_actions_executed == pytest.approx(1 / 20)

#     def test_budget_exhaustion_raises(self, parser, pddl_files):
#         # Create a problem with budget=1
#         problem = PDDLProblem.load_from_pddl(
#             parser, pddl_files["simple"], max_actions=1
#         )
#         action = problem.applicable_ground_actions()[0]
#         problem.apply_action(action)
#         # Second action should raise
#         actions = problem.applicable_ground_actions()
#         if actions:
#             with pytest.raises(ValueError, match="budget"):
#                 problem.apply_action(actions[0])

#     def test_multiple_actions_accumulate_history(self, simple_problem):
#         problem = deepcopy(simple_problem)
#         applied = []
#         for _ in range(3):
#             actions = problem.applicable_ground_actions()
#             if not actions:
#                 break
#             problem.apply_action(actions[0])
#             applied.append(actions[0])
#         assert problem.action_history == applied
#         assert problem.num_actions_executed == len(applied)


# # ===========================================================================
# # 4. PDDLProblemSolver — is_goal_reached
# # ===========================================================================

# class TestGoalReached:

#     def test_goal_not_reached_initially(self, simple_problem):
#         assert not simple_problem.is_goal_reached()

#     def test_goal_reached_after_optimal_solution(self, simple_problem):
#         """
#         Manually apply the known optimal 4-step solution for the simple problem:
#             unstack obj0 obj1 → put-down obj0 → pick-up obj1 → stack obj1 obj0
#         obj0=index 0 (on top), obj1=index 1 (on bottom/table)
#         """
#         problem = deepcopy(simple_problem)

#         # Step 1: unstack obj0 from obj1
#         step1 = ('unstack', (0, 1))
#         assert problem.is_ground_action_applicable(step1)
#         problem.apply_action(step1)

#         assert not problem.is_goal_reached()

#         # Step 2: put-down obj0
#         step2 = ('put-down', (0,))
#         assert problem.is_ground_action_applicable(step2)
#         problem.apply_action(step2)

#         # Step 3: pick-up obj1
#         step3 = ('pick-up', (1,))
#         assert problem.is_ground_action_applicable(step3)
#         problem.apply_action(step3)

#         # Step 4: stack obj1 on obj0
#         step4 = ('stack', (1, 0))
#         assert problem.is_ground_action_applicable(step4)
#         problem.apply_action(step4)

#         assert simple_problem.current_state.num_objects == simple_problem.initial_state.num_objects
#         assert problem.is_goal_reached()
#         assert problem.num_actions_executed == 4


# # ===========================================================================
# # 5. PDDLProblemSolver — reset
# # ===========================================================================

# class TestReset:

#     def test_reset_restores_current_state(self, simple_problem):
#         problem = deepcopy(simple_problem)
#         initial_atoms = problem.initial_state.atoms
#         problem.apply_action(problem.applicable_ground_actions()[0])
#         assert problem.current_state.atoms != initial_atoms
#         problem.reset()
#         assert problem.current_state.atoms == initial_atoms

#     def test_reset_clears_action_history(self, simple_problem):
#         problem = deepcopy(simple_problem)
#         problem.apply_action(problem.applicable_ground_actions()[0])
#         problem.reset()
#         assert problem.action_history == []
#         assert problem.num_actions_executed == 0

#     def test_reset_allows_resolving(self, simple_problem):
#         problem = deepcopy(simple_problem)
#         # Apply the optimal solution
#         for action in [('unstack',(0,1)), ('put-down',(0,)), ('pick-up',(1,)), ('stack',(1,0))]:
#             problem.apply_action(action)
#         assert problem.is_goal_reached()
#         # Reset and solve again
#         problem.reset()
#         assert not problem.is_goal_reached()
#         assert problem.num_actions_executed == 0

#     def test_reset_does_not_change_goal(self, simple_problem):
#         problem = deepcopy(simple_problem)
#         goal_before = problem.goal
#         problem.apply_action(problem.applicable_ground_actions()[0])
#         problem.reset()
#         assert problem.goal == goal_before


# # ===========================================================================
# # 6. PDDLProblemSolver — deepcopy isolation
# # ===========================================================================

# class TestDeepCopy:

#     def test_deepcopy_is_independent(self, simple_problem):
#         copy = deepcopy(simple_problem)
#         copy.apply_action(copy.applicable_ground_actions()[0])
#         # Original must be untouched
#         assert simple_problem.num_actions_executed == 0
#         assert simple_problem.current_state.atoms == simple_problem.initial_state.atoms

#     def test_deepcopy_preserves_goal(self, simple_problem):
#         copy = deepcopy(simple_problem)
#         assert copy.goal == simple_problem.goal


# # ===========================================================================
# # 7. ProblemSolver with RandomPolicy — integration
# # ===========================================================================

# class TestProblemSolverWithRandomPolicy:

#     @pytest.fixture
#     def solver(self, parser):
#         policy = RandomPolicy()
#         return ProblemSolver(parser, policy)

#     def test_solve_single_problem_terminates(self, solver, simple_problem):
#         is_solved, info, trajectories, elapsed = solver.solve_problems(
#             [simple_problem], list_max_actions=30
#         )
#         assert len(is_solved) == 1
#         assert len(trajectories) == 1
#         assert elapsed > 0

#     def test_solve_returns_correct_number_of_results(self, solver, simple_problem, tower_problem):
#         problems = [simple_problem, tower_problem]
#         is_solved, info, trajectories, _ = solver.solve_problems(problems, list_max_actions=50)
#         assert len(is_solved) == 2
#         assert len(info) == 2
#         assert len(trajectories) == 2

#     def test_trajectory_steps_have_required_keys(self, solver, simple_problem):
#         _, _, trajectories, _ = solver.solve_problems([simple_problem], list_max_actions=20)
#         required_keys = {
#             'state', 'internal_state', 'applicable_actions',
#             'chosen_action', 'chosen_action_ind', 'action_log_prob', 'reward',
#         }
#         for step in trajectories[0]:
#             assert required_keys.issubset(step.keys()), \
#                 f"Step missing keys: {required_keys - step.keys()}"

#     def test_chosen_action_is_in_applicable_actions(self, solver, simple_problem):
#         _, _, trajectories, _ = solver.solve_problems([simple_problem], list_max_actions=20)
#         for step in trajectories[0]:
#             assert step['chosen_action'] in step['applicable_actions']

#     def test_chosen_action_ind_matches_chosen_action(self, solver, simple_problem):
#         _, _, trajectories, _ = solver.solve_problems([simple_problem], list_max_actions=20)
#         for step in trajectories[0]:
#             action = step['chosen_action']
#             ind = step['chosen_action_ind']
#             assert step['applicable_actions'][ind] == action

#     def test_trajectory_length_respects_budget(self, solver, simple_problem):
#         max_actions = 10
#         _, _, trajectories, _ = solver.solve_problems([simple_problem], list_max_actions=max_actions)
#         assert len(trajectories[0]) <= max_actions

#     def test_problem_is_reset_before_solving(self, solver, simple_problem):
#         """solve_problems must reset each problem, making it idempotent."""
#         _, _, traj1, _ = solver.solve_problems([simple_problem], list_max_actions=20)
#         _, _, traj2, _ = solver.solve_problems([simple_problem], list_max_actions=20)
#         # Both runs start from the same initial state
#         assert traj1[0]['state'].atoms == traj2[0]['state'].atoms

#     def test_info_dict_has_required_keys(self, solver, simple_problem):
#         _, info, _, _ = solver.solve_problems([simple_problem], list_max_actions=20)
#         required = {'num_steps', 'max_actions', 'goal_reached', 'action_history',
#                     'num_objects', 'num_goal_atoms'}
#         assert required.issubset(info[0].keys())

#     def test_info_num_steps_matches_trajectory_length(self, solver, simple_problem):
#         _, info, trajectories, _ = solver.solve_problems([simple_problem], list_max_actions=20)
#         assert info[0]['num_steps'] == len(trajectories[0])

#     def test_info_action_history_matches_trajectory_actions(self, solver, simple_problem):
#         _, info, trajectories, _ = solver.solve_problems([simple_problem], list_max_actions=20)
#         traj_actions = [step['chosen_action'] for step in trajectories[0]]
#         assert info[0]['action_history'] == traj_actions

#     def test_scalar_max_actions_broadcasts_to_all_problems(self, solver, simple_problem, tower_problem):
#         problems = [simple_problem, tower_problem]
#         _, info, _, _ = solver.solve_problems(problems, list_max_actions=15)
#         assert info[0]['max_actions'] == 15
#         assert info[1]['max_actions'] == 15

#     def test_solve_batch_of_same_problem(self, solver, parser, pddl_files):
#         """Solving 5 independent copies of the same problem should work."""
#         problems = [
#             PDDLProblem.load_from_pddl(parser, pddl_files["simple"], max_actions=30)
#             for _ in range(5)
#         ]
#         is_solved, info, trajectories, _ = solver.solve_problems(problems, list_max_actions=30)
#         assert len(is_solved) == 5
#         assert all(len(t) > 0 for t in trajectories)

#     def test_random_policy_eventually_solves_simple_problem(self, solver, parser, pddl_files):
#         """
#         With enough budget, a random policy should solve the 2-block problem
#         at least once in 20 independent runs (the probability of failure is negligible).
#         """
#         solved_any = False
#         for _ in range(20):
#             problem = PDDLProblem.load_from_pddl(
#                 parser, pddl_files["simple"], max_actions=100
#             )
#             is_solved, _, _, _ = solver.solve_problems([problem], list_max_actions=100)
#             if is_solved[0]:
#                 solved_any = True
#                 break
#         assert solved_any, "Random policy never solved the simple 2-block problem in 20 attempts"


# # ===========================================================================
# # 8. PDDLState sanity checks (independent of solver)
# # ===========================================================================

# class TestPDDLState:

#     def test_state_num_objects_matches_problem(self, simple_problem):
#         state = simple_problem.current_state
#         assert state.num_objects == 2

#     def test_state_atoms_are_a_set(self, simple_problem):
#         assert isinstance(simple_problem.current_state.atoms, set)

#     def test_add_and_del_atom(self, simple_problem):
#         state = simple_problem.current_state  # deep copy via property
#         # 'ontable' is a unary predicate — obj0 is already on the table
#         # We remove it and check it disappears
#         atom = ('ontable', (0,))
#         if atom in state.atoms:
#             state.del_atom(atom)
#             assert atom not in state.atoms

#     def test_num_atoms_each_type_sums_to_total(self, simple_problem):
#         state = simple_problem.current_state
#         assert sum(state.num_atoms_each_type) == state.num_atoms

#     def test_num_objects_each_type_sums_to_total(self, simple_problem):
#         state = simple_problem.current_state
#         assert sum(state.num_objects_each_type) == state.num_objects
