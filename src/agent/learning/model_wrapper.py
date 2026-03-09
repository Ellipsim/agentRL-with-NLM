"""
> model_wrapper_solver.py

Adaptation of model_wrapper.py for use by a solving agent.

Key changes vs. the generation version:
  - NLMWrapper.obtain_internal_state_encodings() always uses
    atoms_nlm_encoding_with_goal_state(current_state, goal_state).
    The init/goal phase branching is gone entirely.
  - No virtual objects (not needed for solving).
  - Extra nullary predicates reference PDDLProblemSolver attributes
    (perc_actions_executed, max_actions) instead of the generation-phase
    equivalents (perc_init_state_actions_executed, max_actions_init_phase).
  - NLMWrapperActor and NLMWrapperCritic are otherwise unchanged.
"""

from typing import Union, List, Tuple, Optional, Any
Action = Tuple[str, Tuple[int, ...]]

from copy import deepcopy
from abc import ABC, abstractmethod
import torch
import argparse

from src.agent.pddl.pddl_problem import PDDLProblem
from src.agent.learning.data_utils import pad_nlm_state, stack_nlm_states
from neural_logic_machine import NLM


# ---------------------------------------------------------------------------
# Abstract base (unchanged from generation version)
# ---------------------------------------------------------------------------

class ModelWrapper(ABC, torch.nn.Module):
    def __init__(self, args: Union[argparse.Namespace, dict], model_arguments: dict):
        super().__init__()
        self.args = self._get_args_dict(args)

    # Auxiliary method for copying and representing args as a dictionary (instead of argparse.Namespace)
    @staticmethod
    def _get_args_dict(args:Union[argparse.Namespace, dict]):
        args_dict = deepcopy(args) if type(args) == dict else deepcopy(vars(args))
        return args_dict

    @abstractmethod
    def obtain_internal_state_encodings(self, problems: List[PDDLProblem]) -> List[Any]:
        """
        Given a list of PDDLProblem objects, it returns a list with the internal state encodings used by the ML model.
        It needs to return a separate encoding for each problem, since when training the policy we will append
        the internal encodings of a different number of samples depending on the batch size.
        """
        raise NotImplementedError

    @staticmethod
    def add_model_specific_args(parent_parser):
        # See https://lightning.ai/docs/pytorch/1.6.2/common/hyperparameters.html
        # Each model wrapper should parse its model specific parameters (e.g., for NLM, the number of layers)
        raise NotImplementedError

    @abstractmethod
    def forward(self):
        """
        For the actor policies, it outputs the log probabilities for the actions in applicable_actions_list. It also outputs a list with the
        internal state representation of the model for each problem.
        For the critic policies, it outputs the state-value V(s) for each problem.
        """
        raise NotImplementedError


# ---------------------------------------------------------------------------
# Shared NLM wrapper base
# ---------------------------------------------------------------------------

class NLMWrapper(ModelWrapper):
    """
    NLM wrapper for the solving agent.

    The state encoding is always:
        current_state || goal_state   (via atoms_nlm_encoding_with_goal_state)

    No virtual objects are added — the agent operates on the concrete objects
    of the problem, just like the generation goal phase did.
    """

    def __init__(self, args: Union[argparse.Namespace, dict], model_arguments: dict, device):
        super().__init__(args, model_arguments)

        # dummy_pddl_state is a PDDLState built from the domain's predicates/actions.
        # For the actor it carries predicate metadata; for the critic it is only used
        # for arity information.
        self.dummy_pddl_state = model_arguments["dummy_pddl_state"]
        self.device = device

        # Initialize NLM
        hidden_features = [[self.args['hidden_features']] * (self.args['breadth'] + 1)] * (self.args['depth'] - 1)
        out_features = self._get_nlm_out_features()
        residual = None if self.args['residual'] == 'no' else self.args['residual']

        self.model = NLM(hidden_features,
                         out_features,
                         self.args['mlp_hidden_features'],
                         residual,
                         self.args['exclude_self'],
                         self.args['use_batch_norm'],
                         self.args['activation'],
        )

    def _get_nlm_out_features(self):
        raise NotImplementedError

    @staticmethod
    def add_model_specific_args(parser):
        """Identical to the generation version — NLM hyperparameters are unchanged."""
        parser.set_defaults(ML_model="NLM")
        parser.add_argument('--breadth', default=3, type=int, help="Maximum arity of predicates in the NLM.")
        parser.add_argument('--depth', default=5, type=int, help="Number of NLM layers.")
        parser.add_argument('--hidden-features', default=8, type=int, help=("Number of predicates for each arity output by all the NLM layers except the final one." 
                                                                           "Right now, we assume the same number of predicates for all inner layers and arities."))
        parser.add_argument('--mlp-hidden-features', default=0, type=int, help="Units in the hidden layer of all the inference MLPs. If 0, the inference MLPs have no hidden layer.")
        parser.add_argument('--residual', default="input", choices=["no", "all", "input"], help=("Residual connections. If 'no', no residual is used."
                                                                                                 "If 'all', each layer receives as additional input the inputs of all the previous layers."
                                                                                                 "If 'input', each layer receives as additional input the input of the first layer."))
        parser.add_argument('--exclude-self', default=True, type=eval, help="If True, the reduce operation ignores tensor positions corresponding to repeated indexes (e.g., [5][5][3] or [2][2][0][1]).")
        parser.add_argument('--use-batch-norm', action="store_true", help="If this argument is provided, we apply batch normalization to the output of the inference MLPs.")
        parser.add_argument('--activation', default='sigmoid', choices=["sigmoid", "relu"], help="Activation function for the inference MLPs. The options are: 'sigmoid' and 'relu'.")
        
        # Extra nullary predicates
        parser.add_argument('--input-max-size', action="store_true", help=("If this argument is provided, the NLM receives as additional input the maximum number of actions that can be executed"
                                                                           "in the init or in the init and goal phases (depending on whether we are in the init or goal generation phase)."
                                                                           "This number is multiplied by 0.1."))
        parser.add_argument('--input-num-actions', default=True, type=eval, help=("If True, the NLM receives as additional input the percentage of actions executed in the init or in the init+goal phases"   
                                                                                  "(depending on the current phase), when compare to the maximum number of available actions."))
        parser.add_argument('--input-num-objs', default=True, type=eval, help="If True, the NLM receives as additional input the number of objects of each type in the state (normalized by max actions init phase).")
        parser.add_argument('--input-num-atoms', default=True, type=eval, help=("If True, the NLM receives as additional input the number of atoms of each type in the init state or the init and goal states"
                                                                                "(depending on the current phase), always normalized by max actions init phase."))

    # ------------------------------------------------------------------
    # Extra nullary predicates
    # ------------------------------------------------------------------

    #TODO: revisar en más detalle
    def _obtain_extra_nullary_predicates(self, problems: List[PDDLProblem]) -> List[List[float]]:
        """
        Build the list of extra nullary scalar inputs for each problem.

        Mapping from generation → solving:
            max_actions_init_phase  →  max_actions
            perc_init_state_actions_executed  →  perc_actions_executed
            _initial_state.*  →  current_state.*   (for atom counts)
            _goal_state.*     →  _goal_state.*      (unchanged)
        """
        num_problems = len(problems)
        extra = [[] for _ in range(num_problems)]

        if self.args['input_max_size']:
            # Single budget value (solver has one phase, not two)
            extra = [e + [p.max_actions * 0.1] for e, p in zip(extra, problems)] # TODO: Por qué noramaiza por 0.1?

        if self.args['input_num_actions']:
            # Fraction of budget consumed so far
            extra = [e + [p.perc_actions_executed] for e, p in zip(extra, problems)]

        if self.args['input_num_objs']:
            # Per-type object counts normalised by max_actions
            extra = [e + [n / p.max_actions for n in p.current_state.num_objects_each_type] for e, p in zip(extra, problems)]

        if self.args['input_num_atoms']:
            # Atom counts for both current state and goal state, normalised by max_actions.
            # This mirrors what the generation goal phase did with init+goal atom counts.
            extra = [e + [n / p.max_actions for n in p.current_state.num_atoms_each_type]
                       + [n / p.max_actions for n in p._goal_state.num_atoms_each_type] # TODO: Revisar _goal
                       for e, p in zip(extra, problems)
            ]

        return extra

    # ------------------------------------------------------------------
    # State encoding
    # ------------------------------------------------------------------

    def obtain_internal_state_encodings(self, problems: List[PDDLProblem]) -> List[Tuple]:
        """
        Encode each problem as (current_state || goal_state) using the NLM tensor format.

        This always uses atoms_nlm_encoding_with_goal_state — there is no init/goal
        phase branching needed for solving.  Virtual objects are never added.
        """
        extra_nullary_preds_list = self._obtain_extra_nullary_predicates(problems)

        list_state_encodings = [problems[i].current_state.atoms_nlm_encoding_with_goal_state(
                problems[i]._goal_state,
                self.device,
                self.args['breadth'],
                add_object_types=True,
                extra_nullary_predicates=extra_nullary_preds_list[i],
            )
            for i in range(len(problems))
        ]

        # Number of objects is the same in current_state and goal_state (no virtuals)
        list_num_objs = [p.current_state.num_objects for p in problems]

        internal_state_list = [(s, n) for s, n in zip(list_state_encodings, list_num_objs)]

        return internal_state_list

    # ------------------------------------------------------------------
    # Batching helper (unchanged)
    # ------------------------------------------------------------------

    @staticmethod
    def stack_state_encodings(list_state_encodings: List[List[Optional[torch.Tensor]]], list_num_objs: List[int],) \
        -> List[Optional[torch.Tensor]]:
        max_num_objs = max(list_num_objs)
        
        list_padded_state_encodings = [pad_nlm_state(tensor_list, max_num_objs) for tensor_list in list_state_encodings]
        batch_state_encoding = stack_nlm_states(list_padded_state_encodings)
        return batch_state_encoding


# ---------------------------------------------------------------------------
# Actor
# ---------------------------------------------------------------------------

class NLMWrapperActor(NLMWrapper):
    """
    NLM actor for the solving agent.
    Maps (current_state || goal_state) → log-probabilities over applicable actions.
    Logic is identical to the generation version; only obtain_internal_state_encodings differs.
    """

    def _get_nlm_out_features(self):
        num_preds_each_arity = self.dummy_pddl_state.num_preds_each_arity
        out_features = [num_preds_each_arity[ar] if ar in num_preds_each_arity else 0 \
                        for ar in range(self.args['breadth'] + 1)]
        
        return out_features

    def _get_nlm_output_applicable_actions(self, nlm_output: List[Optional[torch.Tensor]], applicable_actions_list: List[Tuple[Action]]) \
        -> List[torch.Tensor]:
        # TODO: Pasamos acciones como predicados (Legacy: NeSIG)
        action_name_to_ind = self.dummy_pddl_state.pred_names_to_indices_dict_each_arity
        num_problems = len(applicable_actions_list)

        applicable_actions_nlm_output = [torch.stack([nlm_output[len(action[1])][(problem_ind,) + action[1] + (action_name_to_ind[action[0]],)] \
                                                      for action in applicable_actions_list[problem_ind]]) \
                                        for problem_ind in range(num_problems)]
        
        return applicable_actions_nlm_output

    def _log_softmax(self, applicable_actions_nlm_output: List[torch.Tensor]) -> List[torch.Tensor]:
        applicable_actions_log_probs = [t - torch.logsumexp(t, dim=-1) for t in applicable_actions_nlm_output]
        return applicable_actions_log_probs

    def forward(self, problems: List[Union[PDDLProblem, Tuple]], applicable_actions_list: List[Tuple[Action]],) \
        -> Tuple[List[torch.Tensor], List[Tuple]]:

        num_problems = len(problems)

        assert num_problems > 0
        assert num_problems == len(applicable_actions_list)
        for action_list in applicable_actions_list:
            assert len(action_list)>0, f"A problem has no applicable actions!"

        if isinstance(problems[0], PDDLProblem):
            internal_state_list = self.obtain_internal_state_encodings(problems)
        elif isinstance(problems[0], tuple):
            internal_state_list = problems
        else:
            raise TypeError(
                f"actor.forward expected problems to be List[PDDLProblem] or List[tuple], "
                f"but received List[{type(problems[0]).__name__}]"
            )

        list_state_encodings = [s[0] for s in internal_state_list]
        list_num_objs = [s[1] for s in internal_state_list]

        assert all(n > 0 for n in list_num_objs), "States cannot have 0 objects!"

        batch_state_encoding = self.stack_state_encodings(list_state_encodings, list_num_objs)
        nlm_output = self.model(batch_state_encoding, list_num_objs)

        applicable_actions_nlm_output = self._get_nlm_output_applicable_actions(nlm_output, applicable_actions_list)
        
        applicable_actions_log_probs = self._log_softmax(applicable_actions_nlm_output)

        return applicable_actions_log_probs, internal_state_list


# ---------------------------------------------------------------------------
# Critic
# ---------------------------------------------------------------------------

class NLMWrapperCritic(NLMWrapper):
    """
    NLM critic for the solving agent.
    Maps (current_state || goal_state) → scalar state value V(s).
    Identical to the generation version except for obtain_internal_state_encodings.
    """

    def _get_nlm_out_features(self):

        out_features = [1] + [0] * self.args['breadth']
        return out_features

    def forward(self, problems: List[Union[PDDLProblem, Tuple]]) -> Tuple[List[torch.Tensor], List[Tuple]]:
        
        assert len(problems) > 0

        if isinstance(problems[0], PDDLProblem):
            internal_state_list = self.obtain_internal_state_encodings(problems)
        elif isinstance(problems[0], tuple):
            internal_state_list = problems
        else:
            raise TypeError("critic: problems must be List[PDDLProblemSolver] or List[tuple]")

        list_state_encodings = [s[0] for s in internal_state_list]
        list_num_objs = [s[1] for s in internal_state_list]
        batch_state_encoding  = self.stack_state_encodings(list_state_encodings, list_num_objs)
        nlm_output = self.model(batch_state_encoding , list_num_objs)

        # Single nullary output = V(s)
        state_values = [nlm_output[0][i, 0] for i in range(len(problems))]
        return state_values, internal_state_list