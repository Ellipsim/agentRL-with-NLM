"""
> pddl_problem_solver.py

Adaptation of PDDLProblem for use by an agent whose objective is to *solve*
a given PDDL Blocksworld problem (rather than generate one).

Key design decisions vs. the original NeSIG PDDLProblem:
  - The agent works on `current_state`, which starts as `initial_state` and
    is mutated step-by-step toward the `goal`.
  - All generation-phase machinery (goal_state generation, virtual objects,
    init/goal phase flags) has been removed.
  - New solver primitives added:
      * applicable_ground_actions()   – actions legal at the *current* state
      * applicable_lifted_actions()   – lifted names of the above
      * is_ground_action_applicable() – single-action applicability check
      * apply_action()                – advance current_state by one action
      * is_goal_reached()             – termination check
      * action_history                – full trajectory so far
      * reset()                       – restart from initial_state
  - load_from_pddl() and dump_to_pddl() are kept as useful I/O utilities.
"""

from typing import List, Tuple, Optional
from pathlib import Path
from copy import deepcopy

from src.agent.pddl.pddl_state import PDDLState


class PDDLProblem:
    """
    Represents a PDDL problem to be *solved* by an agent.

    The agent calls `apply_action()` repeatedly, advancing `current_state`
    from `initial_state` until `is_goal_reached()` returns True.

    Typical usage::

        problem = PDDLProblemSolver.load_from_pddl(parser, "problem.pddl")

        while not problem.is_goal_reached():
            actions = problem.applicable_ground_actions()
            chosen  = my_agent.select(actions, problem)
            problem.apply_action(chosen)

        print("Solved in", problem.num_actions_executed, "steps")
        print("Plan:", problem.action_history)
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        parser,
        initial_state: Optional[PDDLState] = None,
        goal: Optional[tuple] = None,
        goal_state: Optional[PDDLState] = None,
        max_actions: Optional[int] = None,
    ):
        """
        Parameters
        ----------
        parser
            An instance of ``lifted_pddl.Parser`` already initialised with
            ``parser.parse_domain(domain_path)``.
        initial_state
            The starting PDDLState.  If None an empty state is used.
        goal
            A tuple of atoms (sorted) that must all be true for the problem to
            be considered solved.  Each atom has the form ``(pred_name, (obj_idx, …))``.
        max_actions
            Optional upper bound used to compute ``perc_actions_executed``.
        """
        self.parser = deepcopy(parser)
        self.max_actions = max_actions

        # The initial state never changes after construction.
        self._initial_state: PDDLState = (
            deepcopy(initial_state)
            if initial_state is not None
            else PDDLState(parser.types, parser.type_hierarchy, parser.predicates)
        )

        # Mirror the type/predicate ordering from the state (important for
        # methods that depend on ordering, e.g. get_continuous_consistent_…).
        self.types = self._initial_state.types
        self.type_hierarchy = self._initial_state.type_hierarchy
        self.predicates = self._initial_state.predicates

        # The goal is a frozenset of atoms that the agent must achieve.
        self._goal: Optional[tuple] = goal  # tuple of sorted atoms
        self._goal_state = (    #TODO: Revisar goal state
            deepcopy(goal_state)
            if goal_state is not None
            else PDDLState(parser.types, parser.type_hierarchy, parser.predicates, list(parser.object_types), goal)
        )

        # The current state starts as a deep copy of the initial state and is
        # mutated by apply_action().
        self._current_state: PDDLState = deepcopy(self._initial_state)
        

        # Trajectory bookkeeping.
        self._action_history: List[Tuple[str, Tuple[int, ...]]] = []

    # ------------------------------------------------------------------
    # Class-method constructors
    # ------------------------------------------------------------------

    @classmethod
    def load_from_pddl(cls, _parser, problem_path: Path, max_actions: Optional[int] = None):
        """
        Load a fully-specified PDDL problem from disk.

        The parser must already have the domain loaded via
        ``parser.parse_domain(domain_path)``.
        """

        # TODO: MUY IMPORTANTE, DEEP COPY TIENE UN BUG Y NO COPIA LAS CONSTATES, ESTAR ATENTO POR SI CAUSA PROBLEMAS EN EL FUTURO
        parser = deepcopy(_parser)
        parser.parse_problem(str(problem_path))

        initial_state = PDDLState(
            parser.types,
            parser.type_hierarchy,
            parser.predicates,
            objects=list(parser.object_types),
            atoms=set(parser.atoms),
        ) 

        # parser.goals entries are (is_true, pred_name, (obj0, obj1)); convert to
        # (pred_name, (obj0, obj1, …)) to match the atom format used by PDDLState.
        # Skip the first element (is_true flag)
        goal = set(goal[1:] for goal in parser.goals)
        goal_state = PDDLState( #TODO: revisar goal state
            parser.types,
            parser.type_hierarchy,
            parser.predicates,
            objects=list(parser.object_types),
            atoms=goal,
        ) 

        return cls(parser, initial_state=initial_state, goal=goal, goal_state=goal_state, max_actions=max_actions)

    # ------------------------------------------------------------------
    # Properties – read-only views of internal state
    # ------------------------------------------------------------------

    @property
    def initial_state(self) -> PDDLState:
        """The immutable starting state of the problem."""
        return deepcopy(self._initial_state)

    @property
    def current_state(self) -> PDDLState:
        """The state the agent is currently in."""
        return deepcopy(self._current_state)

    @property
    def goal(self) -> Optional[tuple]:
        """The set of atoms the agent must achieve."""
        return deepcopy(self._goal)

    @property
    def goal_state(self) -> PDDLState:
        """The target goal state to reach."""
        return deepcopy(self._goal_state)

    @property
    def action_history(self) -> List[Tuple[str, Tuple[int, ...]]]:
        """Ordered list of ground actions applied so far."""
        return list(self._action_history)  # shallow copy is fine – tuples are immutable

    @property
    def num_actions_executed(self) -> int:
        """Number of actions applied since construction (or last reset)."""
        return len(self._action_history)

    @property
    def perc_actions_executed(self) -> float:
        """Fraction of max_actions consumed.  Requires max_actions to be set."""
        if self.max_actions is None:
            raise ValueError("max_actions must be set to compute perc_actions_executed")
        return self.num_actions_executed / self.max_actions

    # ------------------------------------------------------------------
    # Internal helper
    # ------------------------------------------------------------------

    def _sync_parser_to_current_state(self) -> None:
        """
        Point the parser's internal state at self._current_state so that
        get_applicable_actions / get_next_state operate on the right state.
        """
        self.parser.object_names = []          # not needed for action queries
        self.parser.object_types = self._current_state.objects
        self.parser.atoms = self._current_state.atoms
        self.parser.goals = set()              # not needed for action queries

    # ------------------------------------------------------------------
    # Solver primitives
    # ------------------------------------------------------------------

    def applicable_ground_actions(self) -> Tuple[Tuple[str, Tuple[int, ...]], ...]:
        """
        Return all ground domain actions that are applicable at ``current_state``.

        Actions with repeated object indices (e.g. ``stack(A, A)``) are excluded.
        The result is a sorted, immutable tuple of ``(action_name, (obj_idx, …))``
        pairs.
        """
        self._sync_parser_to_current_state()

        raw = self.parser.get_applicable_actions()  # dict: name -> list of param tuples

        actions = [
            (name, param)
            for name, params in raw.items()
            for param in params 
            if len(param) == len(set(param))  # no repeated objects
        ]

        return tuple(sorted(actions))

    def applicable_lifted_actions(self) -> List[str]:
        """
        Return the names of all lifted actions that have at least one applicable
        grounding at ``current_state``.
        """
        ground = self.applicable_ground_actions()
        seen = []
        for name, _ in ground:
            if name not in seen:
                seen.append(name)
        return seen

    def is_ground_action_applicable(
        self, ground_action: Tuple[str, Tuple[int, ...]]
    ) -> bool:
        """
        Check whether a single ground action is applicable at ``current_state``.

        Parameters
        ----------
        ground_action
            E.g. ``('stack', (1, 2))``.
        """
        self._sync_parser_to_current_state()
        return self.parser.is_action_applicable(
            ground_action[0], tuple(ground_action[1])
        )

    def apply_action(self, ground_action: Tuple[str, Tuple[int, ...]]) -> None:
        """
        Apply a ground action to ``current_state``, advancing the agent by one step.

        The action is assumed to be applicable; call ``is_ground_action_applicable``
        first if you are not certain.

        Parameters
        ----------
        ground_action
            E.g. ``('stack', (1, 2))``.

        Raises
        ------
        ValueError
            If max_actions is set and has already been reached.
        """
        if self.max_actions is not None and self.num_actions_executed >= self.max_actions:
            raise ValueError(
                f"Action budget exhausted: {self.max_actions} actions already executed."
            )

        self._sync_parser_to_current_state()

        next_atoms = self.parser.get_next_state(
            ground_action[0],
            tuple(ground_action[1]),
            check_action_applicability=False,  # We assume the action is applicable
        )
        self._current_state.atoms = next_atoms
        self._action_history.append(ground_action)

    def is_goal_reached(self) -> bool:
        """
        Return True iff every goal atom is present in ``current_state``.

        An empty or None goal is considered immediately satisfied (useful for
        testing / partial problems).
        """
        if not self._goal:
            return True
        goal_atoms = set(self._goal)
        return goal_atoms.issubset(self._current_state.atoms)

    def reset(self) -> None:
        """
        Restore ``current_state`` to ``initial_state`` and clear action history.
        Useful for running multiple solving attempts on the same problem.
        """
        self._current_state = deepcopy(self._initial_state)
        self._action_history.clear()

    # ------------------------------------------------------------------
    # I/O
    # ------------------------------------------------------------------

    def dump_to_pddl(self, problem_name: Optional[str] = None) -> str:
        """
        Serialise the problem (initial state + goal) to a PDDL string.

        Note: this always uses the *original* initial_state, not the current
        (possibly partially-solved) state.  This is the standard convention for
        reporting the problem being solved.
        """
        domain_name = self.parser.domain_name
        if problem_name is None:
            problem_name = f"problem_{domain_name}"

        objects = self._initial_state.objects
        init_atoms = sorted(self._initial_state.atoms)
        goal_atoms = sorted(self._goal) if self._goal else []

        lines = [
            f"(define (problem {problem_name})\n",
            f"(:domain {domain_name})\n\n",
            "(:objects\n",
        ]

        # Group objects by type
        type_to_indices: dict = {}
        for idx, obj_type in enumerate(objects):
            type_to_indices.setdefault(obj_type, []).append(idx)

        for obj_type, indices in type_to_indices.items():
            obj_names = " ".join(f"obj{i}" for i in indices)
            lines.append(f"\t{obj_names} - {obj_type}\n")
        lines.append(")\n\n")

        lines.append("(:init\n")
        for atom in init_atoms:
            obj_str = " ".join(f"obj{i}" for i in atom[1])
            lines.append(f"\t({atom[0]} {obj_str})\n")
        lines.append(")\n\n")

        lines.append("(:goal (and\n")
        for atom in goal_atoms:
            obj_str = " ".join(f"obj{i}" for i in atom[1])
            lines.append(f"\t({atom[0]} {obj_str})\n")
        lines.append("))\n")
        lines.append(")")

        return "".join(lines)

    # ------------------------------------------------------------------
    # Dunder methods
    # ------------------------------------------------------------------

    def __repr__(self) -> str:
        return (
            f"PDDLProblemSolver("
            f"domain={self.parser.domain_name!r}, "
            f"objects={len(self._initial_state.objects)}, "
            f"goal_atoms={len(self._goal) if self._goal else 0}, "
            f"steps={self.num_actions_executed}, "
            f"solved={self.is_goal_reached()})"
        )

    def __eq__(self, other) -> bool:
        if not isinstance(other, PDDLProblem):
            return False
        return (
            self._initial_state == other._initial_state
            and self._current_state == other._current_state
            and self._goal == other._goal
            and self._goal_state == other._goal_state
            and self._action_history == other._action_history
        )

    def __copy__(self):
        new = PDDLProblem(
            self.parser,
            initial_state=self._initial_state,
            goal=self._goal,
            goal_state=self._goal_state,
            max_actions=self.max_actions,
        )
        new._current_state = deepcopy(self._current_state)
        new._action_history = list(self._action_history)
        return new

    def __deepcopy__(self, memo):
        return self.__copy__()
