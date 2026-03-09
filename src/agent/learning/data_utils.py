"""
> data_utils_solver.py

Adaptation of data_utils.py for the solving agent.

Changes vs. generation version:
  - common_collate_fn: replaces the three generation reward fields
    (consistency_reward, difficulty_reward, diversity_reward) with a single
    'reward' field.  All other fields are unchanged.
  - pad_nlm_state and stack_nlm_states are unchanged and re-exported here
    so the rest of the solver codebase only needs to import from this module.

Trajectory sample dict expected by the collate function:
    state              : PDDLProblemSolver snapshot (before the action)
    internal_state     : NLM encoding tuple (tensor_list, num_objs)
    applicable_actions : Tuple[Action, ...]
    chosen_action      : Action
    chosen_action_ind  : int
    action_log_prob    : float  (log-prob of chosen_action under old policy)
    reward             : float  (shaped or sparse solve reward)
    return             : float  (discounted cumulative reward G_t)
    advantage          : float  (GAE A(s,a))
    state_value        : float  (V(s) under old critic)
"""

from typing import List, Dict, Optional
import torch
from torch.utils.data import Dataset


# ---------------------------------------------------------------------------
# Re-exported unchanged utilities
# ---------------------------------------------------------------------------

def pad_nlm_state(
    X: List[Optional[torch.Tensor]], N: int, pad_val: float = 0
) -> List[Optional[torch.Tensor]]:
    """Pad each arity-r tensor from shape [n^r, P] to [N^r, P]."""
    for r, t in enumerate(X[1:]):
        if t is not None:
            assert t.shape[0] <= N, (
                f"Tensor of arity {r+1} has {t.shape[0]} objects but N={N}"
            )
    return (
        [X[0].clone() if X[0] is not None else None]
        + [
            torch.nn.functional.pad(
                x, pad=(0, 0) + (0, N - x.shape[0]) * (x.dim() - 1),
                mode='constant', value=pad_val,
            )
            if x is not None else None
            for x in X[1:]
        ]
    )


def stack_nlm_states(
    X: List[List[Optional[torch.Tensor]]]
) -> List[Optional[torch.Tensor]]:
    """Stack a batch of (already padded) NLM state encodings."""
    num_tensors = len(X[0])
    return [
        torch.stack([x[r] for x in X], dim=0) if X[0][r] is not None else None
        for r in range(num_tensors)
    ]


# ---------------------------------------------------------------------------
# Dataset
# ---------------------------------------------------------------------------

class SolverDataset(Dataset):
    """Simple list-backed dataset of trajectory step dicts."""

    def __init__(self, sample_list: List[Dict] = []):
        assert isinstance(sample_list, list)
        self._dataset = list(sample_list)

    def __len__(self):
        return len(self._dataset)

    def __getitem__(self, idx):
        return self._dataset[idx]

    def add_element(self, sample: Dict):
        self._dataset.append(sample)

    def del_element(self, idx: int):
        if idx < 0 or idx >= len(self):
            raise ValueError("Index out of range")
        del self._dataset[idx]


# ---------------------------------------------------------------------------
# Collate
# ---------------------------------------------------------------------------

def solver_collate_fn(batch: List[Dict]) -> Dict:
    """
    Collate a list of trajectory step dicts into a single batch dict.

    The three generation-specific reward fields (consistency, difficulty,
    diversity) are replaced by a single 'reward' field.  Everything else
    mirrors the generation collate function.
    """
    return {
        'states':                [s['state']             for s in batch],
        'internal_states':       [s['internal_state']    for s in batch],
        'applicable_actions_list': [s['applicable_actions'] for s in batch],
        'chosen_actions':        [s['chosen_action']     for s in batch],
        'chosen_action_inds':    [s['chosen_action_ind'] for s in batch],
        'action_log_probs':      [s['action_log_prob']   for s in batch],
        # Single reward field (replaces consistency/difficulty/diversity rewards)
        'rewards':               [s['reward']            for s in batch],
        'returns':               [s['return']            for s in batch],
        'advantages':            [s['advantage']         for s in batch],
        'state_values':          [s['state_value']       for s in batch],
    }
