"""
> problem_solver.py

Functionality for solving PDDL problems for a given domain using a learned
(or random) policy.

Adapted from NeSIG's problem_generator.py.  All problem-*generation* logic
(init-state phase, goal-state phase, virtual objects, consistency/diversity
evaluation) has been removed.  What remains is a clean solver loop that:

  1. Loads a pre-specified PDDL problem (initial state + goal).
  2. Runs a policy to select actions at each step.
  3. Records the full (s, a) trajectory.
  4. Terminates when the goal is reached or the action budget is exhausted.
"""

from typing import List, Tuple, Optional, Union, Dict
from copy import deepcopy
import time

from lifted_pddl import Parser

from src.agent.learning.generative_policy import GenerativePolicy
from src.agent.pddl.pddl_problem import PDDLProblem

#TODO: Metrics

class ProblemSolver:
    """
    Solves one or more pre-specified PDDL problems using a given policy.

    The solver runs each problem forward from its initial state, applying
    actions chosen by ``policy`` until either the goal is reached or the
    per-problem action budget is exhausted.

    Typical usage::

        solver = ProblemSolver(parser, policy)
        problems = [PDDLProblem.load_from_pddl(parser, p) for p in paths]
        solved, info, trajectories, elapsed = solver.solve_problems(problems, max_actions=50)
    """

    def __init__(self, parser: Parser, policy: GenerativePolicy):
        """
        Parameters
        ----------
        parser
            A ``lifted_pddl.Parser`` instance already initialised with the
            domain via ``parser.parse_domain(domain_path)``.
        policy
            A ``GenerativePolicy`` used to select actions at each step.
            Its ``select_actions`` method is called with the list of active
            ``PDDLProblemSolver`` instances and their applicable actions.
        """
        self.parser = parser
        self.policy = policy

    # ------------------------------------------------------------------
    # Core solve loop
    # ------------------------------------------------------------------

    def _solve_trajectories(
        self,
        problems: List[PDDLProblem],
        list_max_actions: List[int],
    ) -> Tuple[List[List[Dict]], List[bool]]:
        """
        Run the solve loop over a batch of problems in parallel.

        Each problem is stepped forward independently; problems that finish
        early (goal reached or budget exhausted) are removed from the active
        set.

        Parameters
        ----------
        problems
            List of ``PDDLProblemSolver`` instances, each already reset to
            their initial state.
        list_max_actions
            Per-problem action budget.  ``list_max_actions[i]`` is the maximum
            number of actions that may be applied to ``problems[i]``.

        Returns
        -------
        trajectories
            ``trajectories[i]`` is a list of step-dicts for problem ``i``.
            Each dict has the keys documented in ``solve_problems``.
        is_solved
            ``is_solved[i]`` is True iff problem ``i`` reached its goal.
        """
        num_problems = len(problems)
        trajectories: List[List[Dict]] = [[] for _ in range(num_problems)]
        is_solved = [False] * num_problems
        is_terminated = [False] * num_problems

        while not all(is_terminated):
            # ---- Active problem indices and instances --------------------
            active = [(i, problems[i]) for i in range(num_problems) if not is_terminated[i]]
            active_inds = [x[0] for x in active]
            active_problems = [x[1] for x in active]

            # ---- Collect applicable actions for every active problem -----
            applicable_actions_list = [p.applicable_ground_actions() for p in active_problems]

            # ---- Policy selects one action per active problem ------------
            chosen_actions, action_log_probs, internal_states = (self.policy.select_actions(active_problems, applicable_actions_list))

            # ---- Apply actions and record trajectory samples -------------
            for local_i, (global_i, action) in enumerate(zip(active_inds, chosen_actions)):
                problem = active_problems[local_i]
                applicable = applicable_actions_list[local_i]

                # Snapshot state *before* the action for the trajectory.
                pre_action_state = problem.current_state  # deep-copied by property

                # Advance the problem.
                problem.apply_action(action)

                # Termination conditions.
                goal_reached = problem.is_goal_reached()
                budget_exceeded = (
                    problem.num_actions_executed >= list_max_actions[global_i]
                )

                if goal_reached or budget_exceeded:
                    is_terminated[global_i] = True
                    is_solved[global_i] = goal_reached

                # Record the (s, a, metadata) sample.
                chosen_action_ind = list(applicable).index(action)
                sample = {
                    # State before the action was applied.
                    "state": pre_action_state,
                    # Policy's internal representation (e.g. NLM tensors).
                    "internal_state": internal_states[local_i],
                    # Full set of legal actions at this state.
                    "applicable_actions": applicable,
                    # The action that was chosen.
                    "chosen_action": action,
                    # Index into applicable_actions — useful for log-prob lookup.
                    "chosen_action_ind": chosen_action_ind,
                    # Log-probability assigned by the policy to this action.
                    "action_log_prob": action_log_probs[local_i],
                    # Placeholder reward fields (populate downstream).
                    "reward": 0,
                }
                trajectories[global_i].append(sample)

        return trajectories, is_solved

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def solve_problems(
        self,
        problems: List[PDDLProblem],
        list_max_actions: Union[Tuple[int, ...], int],
    ) -> Tuple[List[bool], List[Dict], List[List[Dict]], float]:
        """
        Attempt to solve a batch of PDDL problems using ``self.policy``.

        Each problem in ``problems`` must already be a fully-initialised
        ``PDDLProblem`` (loaded via ``PDDLProblem.load_from_pddl``
        or constructed manually).  Problems are reset before solving, so this
        method is safe to call multiple times on the same list.

        Parameters
        ----------
        problems
            List of problems to solve.
        list_max_actions
            Per-problem action budget.  A single ``int`` applies the same
            budget to every problem.

        Returns
        -------
        is_solved
            ``is_solved[i]`` is True iff problem ``i`` reached its goal.
        problem_info_list
            One dict per problem with the keys:

            - ``"num_steps"``: number of actions applied before termination.
            - ``"max_actions"``: the budget that was used.
            - ``"goal_reached"``: same as ``is_solved[i]``.
            - ``"action_history"``: the ordered list of applied actions.
            - ``"num_objects"``: dict mapping type-name → count.
            - ``"num_goal_atoms"``: number of atoms in the goal.

        trajectories
            ``trajectories[i]`` is the list of step-dicts for problem ``i``.
            Each step-dict contains:

            - ``"state"``: ``PDDLState`` snapshot *before* the action.
            - ``"internal_state"``: policy's internal representation.
            - ``"applicable_actions"``: tuple of legal ground actions.
            - ``"chosen_action"``: the action that was applied.
            - ``"chosen_action_ind"``: index of the action in ``applicable_actions``.
            - ``"action_log_prob"``: log-probability from the policy.
            - ``"reward"``: placeholder (0); populate with shaped reward downstream.

        elapsed
            Wall-clock time (seconds) for the entire solve pass, excluding
            any post-hoc analysis.
        """
        assert len(problems) > 0, "problems must be a non-empty list"

        num_problems = len(problems)

        # Normalise budget to a per-problem list.
        if isinstance(list_max_actions, int):
            list_max_actions = (list_max_actions,) * num_problems
        assert len(list_max_actions) == num_problems, ("list_max_actions must be an int or a sequence of length num_problems")

        # Reset every problem to its initial state so solve_problems idempotent when called multiple times on the same list.
        for p in problems : 
            p.reset()

        start_time = time.time()

        trajectories, is_solved = self._solve_trajectories(problems, list(list_max_actions))

        elapsed = time.time() - start_time

        # Build per-problem summary dicts.
        problem_info_list = []
        for i, problem in enumerate(problems):
            obj_types = problem.initial_state.types
            num_objects = {}
            for t in set(obj_types):
                num_objects[t] = obj_types.count(t)

            problem_info_list.append(
                {
                    "num_steps": problem.num_actions_executed,
                    "max_actions": list_max_actions[i],
                    "goal_reached": is_solved[i],
                    "action_history": problem.action_history,
                    "num_objects": num_objects,
                    "num_goal_atoms": len(problem.goal) if problem.goal else 0,
                }
            )

        return is_solved, problem_info_list, trajectories, elapsed