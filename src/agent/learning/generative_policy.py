"""
> solver_policy.py

Adaptation of generative_policy.py for a PDDL solving agent trained with PPO.

Key changes vs. the generation version:
  - Phase is now 'solve' (single phase) instead of 'init'/'goal'.
    get_hparam() no longer needs a phase prefix.
  - PPOPolicy.training_step() is unchanged — the PPO math is identical.
  - common_collate_fn replaces the three generation-specific reward fields
    (consistency/difficulty/diversity) with a single 'reward' field.
  - RandomPolicy is kept as a useful baseline.
"""

from typing import List, Tuple, Dict, Optional, Union, Any
from abc import ABC, abstractmethod
from copy import deepcopy
import math
import argparse

import torch
import pytorch_lightning as pl

Action = Tuple[str, Tuple[int, ...]]

from src.agent.pddl.pddl_problem import PDDLProblem

# ---------------------------------------------------------------------------
# Abstract base
# ---------------------------------------------------------------------------

class GenerativePolicy(ABC, pl.LightningModule):
    """
    Abstract base class for solving policies.

    Subclasses must implement:
        forward()        — returns (log_probs_list, internal_state_list)
        training_step()  — PPO update step
    """

    @abstractmethod
    def forward(self, problems: List[Union[PDDLProblem, Any]], applicable_actions_list: List[Tuple[Action]],) \
        -> Tuple[List[torch.Tensor], List]:
        raise NotImplementedError

    @abstractmethod
    def training_step(self, train_batch, batch_idx=0):
        raise NotImplementedError

    def select_actions(self, problems: List[PDDLProblem], applicable_actions_list: List[Tuple[Action]],) \
        -> Tuple[List[Action], List[torch.Tensor], List[Any]]:
        """
        Run forward() and sample one action per problem.
        Returns (chosen_actions, log_probs, internal_states).
        """
        log_probs_list, internal_state_list = self.forward(problems, applicable_actions_list)

        chosen_actions, chosen_log_probs = [], []

        for log_probs, applicable in zip(log_probs_list, applicable_actions_list):
            idx = torch.multinomial(torch.exp(log_probs), 1).item()
            chosen_actions.append(applicable[idx])
            chosen_log_probs.append(log_probs[idx])

        return chosen_actions, chosen_log_probs, internal_state_list

    @classmethod
    def add_model_specific_args(cls, parser):
        pass


# ---------------------------------------------------------------------------
# Random baseline
# ---------------------------------------------------------------------------

class RandomPolicy(GenerativePolicy):
    """Uniform-random policy. Useful for sanity-checking the solve loop."""

    def __init__(self):
        super().__init__()
        # Not needed
        # assert term_action_prob >= 0 and term_action_prob <= 1, "Probability of selecting TERM_ACTION must be between 0 and 1"
        # self.term_action_prob = term_action_prob

    def forward(self, problems, applicable_actions_list):
        assert len(problems) == len(applicable_actions_list), "Number of problems and number of lists of applicable actions must be the same"
        assert len(problems) > 0, "There must be at least one problem"
        assert all([len(applicable_actions) > 0 for applicable_actions in applicable_actions_list]), \
            "Each list of applicable actions must be non-empty"

        log_probs_list = []

        for applicable in applicable_actions_list:
            n = len(applicable)
            log_probs_list.append(torch.log(torch.ones(n, dtype=torch.float32, requires_grad=False, device=self.device) / n))

        internal_state_list = [deepcopy(p) for p in problems]
        return log_probs_list, internal_state_list

    def training_step(self, train_batch, batch_idx=0):
        raise NotImplementedError("RandomPolicy does not support training")


# ---------------------------------------------------------------------------
# PPO policy
# ---------------------------------------------------------------------------

class PPOSolverPolicy(GenerativePolicy):
    """
    PPO-trained actor-critic policy for PDDL solving.

    The PPO mathematics (clipped surrogate, GAE advantages, entropy bonus)
    are identical to the generation version.  The only structural change is
    the removal of the init/goal phase distinction — there is now a single
    'solve' phase with its own set of hyperparameters.
    """

    def __init__(self, args: argparse.Namespace, actor_class, actor_arguments: dict,
        critic_class, critic_arguments: dict, device): 
        super().__init__()
        self.save_hyperparameters(args)

        self.actor = actor_class(args, actor_arguments, device)
        self.critic = critic_class(args, critic_arguments, device)

        # Logging accumulators (reset after each trainer.fit() call)
        self.total_norm_actor_sum = 0.0
        self.total_norm_critic_sum = 0.0
        self.critic_loss_sum = 0.0
        self.ppo_loss_sum = 0.0
        self.entropy_loss_sum = 0.0
        self.policy_entropy_sum = 0.0
        self.num_samples = 0
        # Added for a better logging with PPO metrics
        self.approx_kl_sum = 0.0
        self.clip_fraction_sum = 0.0
        self.num_minibatches = 0

        self.register_buffer('curr_logging_it', torch.tensor(1, dtype=torch.int32, requires_grad=False))

        # Entropy annealing
        entropy_coeffs = self.hparams['solve_entropy_coeffs']

        if type(entropy_coeffs) == float:
            self.register_buffer('curr_entropy_coeff',torch.tensor(entropy_coeffs, dtype=torch.float32, requires_grad=False, device=self.device))
            self.register_buffer('entropy_reduction_val',torch.tensor(0.0, dtype=torch.float32, requires_grad=False, device=self.device))
            self.final_entropy_coeff = entropy_coeffs
        else:
            self.register_buffer('curr_entropy_coeff',torch.tensor(entropy_coeffs[0], dtype=torch.float32, requires_grad=False, device=self.device))
            self.register_buffer('entropy_reduction_val',torch.tensor((entropy_coeffs[0] - entropy_coeffs[1]) / entropy_coeffs[2],
                                                                   dtype=torch.float32, requires_grad=False, device=self.device))
            self.final_entropy_coeff = entropy_coeffs[1]

    # ------------------------------------------------------------------
    # Hyperparameter helpers
    # ------------------------------------------------------------------

    @staticmethod
    def parse_entropy_coeffs(value):
        try:
            val = float(value)
            if val < 0:
                raise argparse.ArgumentTypeError("Must be non-negative")
            return val
        except ValueError:
            pass

        try:
            parts = value.split(',')
            if len(parts) == 3:
                val =  tuple(float(p) for p in parts)

                if val[0] < 0 or val[1] < 0:
                    raise argparse.ArgumentTypeError("Entropy coeffs must be non-negative")
                if val[1] > val[0]:
                    raise argparse.ArgumentTypeError("Initial entropy coeff must be greater than or equal to final entropy coeff")
                if val[2] < 0:
                    raise argparse.ArgumentTypeError("Number of iterations must be non-negative")

                return val
            else:
                raise argparse.ArgumentTypeError("Entropy coeffs must be either a single float or three floats separated by commas")
        except ValueError:
            raise argparse.ArgumentTypeError("Entropy coeffs must be either a single float or three floats separated by commas")
       

    @classmethod
    def add_model_specific_args(cls, parser):
        """
        Single set of solve-phase hyperparameters.
        (Generation used --init-* and --goal-* prefixes for two phases;
        here we use a plain --solve-* prefix for clarity.)
        """
        parser.set_defaults(solve_policy="PPO")
        parser.add_argument('--solve-lr', default=1e-3, type=float, help="Learning rate")
        parser.add_argument('--solve-PPO-epochs', default=3, type=int, help="For each PPO iteration, how many training epochs to use over the dataset of collected trajectories.")
        parser.add_argument('--solve-epsilon', default=0.2, type=float, help="Epsilon parameter used in PPO. The larger it is, the larger policy updates can be.")
        parser.add_argument('--solve-entropy-coeffs', default=0.0, type=cls.parse_entropy_coeffs, help=("Coefficients used for the PPO entropy term and annealing it."
                                                                                        "the first element is the initial value of the entropy coeff,"
                                                                                        "the second element its final value, and the third element the"
                                                                                        "number of trainer.fit() calls to reach the final value"
                                                                                        "Conversely, a single float value can be provided, in which case"
                                                                                        "the entropy coeff will remain constant."))
        parser.add_argument('--solve-lifted-entropy-weight', default=0.5, type=float, help=("Weight of the lifted entropy in the entropy term of PPO, when compared to the ground entropy."
                                                                                        "It must be between 0 and 1, since ground_entropy_weight = 1 - lifted_entropy_weight."))

    # ------------------------------------------------------------------
    # Entropy
    # ------------------------------------------------------------------

    def calculate_entropy(self, _action_log_probs: torch.Tensor, applicable_actions: List[Tuple[str, Tuple[int]]],) \
        -> torch.Tensor:
        """
        Weighted combination of ground entropy and lifted (per-action-name) entropy.
        Identical to the generation version.
        """
        lifted_entropy_weight = self.hparams['solve_lifted_entropy_weight']
        assert lifted_entropy_weight >= 0 and lifted_entropy_weight <= 1
        assert _action_log_probs.dim() == 1

        applicable_actions = list(applicable_actions)
        action_log_probs = _action_log_probs

        assert len(action_log_probs) == len(applicable_actions)
        num_actions = len(action_log_probs)

        if num_actions <= 1:
            return torch.tensor(0.0, dtype=torch.float32, device=self.device)

        action_probs_no_norm = torch.exp(action_log_probs)
        action_probs = action_probs_no_norm / action_probs_no_norm.sum()

        ground_entropy = (torch.distributions.Categorical(probs=action_probs).entropy() / math.log(num_actions))

        action_name_probs = []
        existing_action_names = set([action[0] for action in applicable_actions])

        for action_name in existing_action_names:
            inds = [i for i, action in enumerate(applicable_actions) if action[0]==action_name]
            action_name_probs.append(torch.sum(action_probs[inds]))

        action_name_probs_tensor = torch.stack(action_name_probs)

        # If there is only one lifted action, the lifted_entropy is 0.0
        lifted_entropy = torch.distributions.Categorical(probs = action_name_probs_tensor).entropy() / \
                         math.log(len(existing_action_names)) \
                         if len(existing_action_names) > 1 else torch.tensor(0.0, dtype=torch.float32, device=self.device)
        
        # <Final entropy>
        entropy = lifted_entropy_weight*lifted_entropy + (1-lifted_entropy_weight)*ground_entropy
        return entropy # zero-dimensional torch.Tensor containing a single float

    def anneal_entropy_coeff(self):
        if self.curr_entropy_coeff > self.final_entropy_coeff:
            self.curr_entropy_coeff -= self.entropy_reduction_val

    # ------------------------------------------------------------------
    # Forward / critic
    # ------------------------------------------------------------------

    def forward(self, problems, applicable_actions_list):
        assert len(problems) == len(applicable_actions_list), "Number of problems and number of lists of applicable actions must be the same"
        assert len(problems) > 0, "There must be at least one problem"
        assert all(len(a) > 0 for a in applicable_actions_list), "Each list of applicable actions must be non-empty"
        
        log_probs_list, internal_state_list = self.actor(problems, applicable_actions_list)
        return log_probs_list, internal_state_list

    def calculate_state_values(self, problems):
        assert len(problems) > 0, "There must be at least one problem"

        state_value_list, internal_state_list = self.critic(problems)
        return state_value_list, internal_state_list

    # ------------------------------------------------------------------
    # Optimiser
    # ------------------------------------------------------------------

    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(self.parameters(), lr=self.hparams['solve_lr'], weight_decay=self.hparams.get('weight_decay', 0.0),)
    
        return optimizer 

    # ------------------------------------------------------------------
    # Training step  (PPO math — identical to generation version)
    # ------------------------------------------------------------------

    def training_step(self, train_batch: Dict, batch_idx=0):
        assert isinstance(train_batch, dict)

        old_state_values = torch.tensor(
            train_batch['state_values'], requires_grad=False, device=self.device
        )
        advantages = torch.tensor(
            train_batch['advantages'], requires_grad=False, device=self.device
        )

        # ---- Critic loss (GAE target) ----
        state_value_list, _ = self.calculate_state_values(train_batch['internal_states'])
        new_state_values = torch.stack(state_value_list)
        critic_target = old_state_values + advantages
        critic_loss = (torch.mean((new_state_values - critic_target) ** 2) * self.hparams['critic_loss_weight'])

        # ---- Actor: PPO clipped surrogate ----
        log_probs_list, _ = self.forward(train_batch['internal_states'], train_batch['applicable_actions_list'])
        curr_probs = torch.exp(torch.stack([t[ind] for t, ind in zip(log_probs_list, train_batch['chosen_action_inds'])]))
        old_probs = torch.exp(torch.tensor(train_batch['action_log_probs'], requires_grad=False, device=self.device))
        ratio = curr_probs / old_probs

        epsilon = self.hparams['solve_epsilon']
        ppo_loss = torch.mean(-torch.min(ratio * advantages, \
                              torch.clamp(ratio, 1 - epsilon, 1 + epsilon) * advantages,))
        
        # ---- PPO diagnostics ----
        with torch.no_grad():
            log_ratio = torch.log(ratio)
            approx_kl = -log_ratio.mean().item()  # KL(old || new) ≈ E[-log(new/old)]
            clip_fraction = ((ratio < 1 - epsilon) | (ratio > 1 + epsilon)).float().mean().item()

        # ---- Entropy bonus ----
        policy_entropy = torch.mean(torch.stack([self.calculate_entropy(lp, actions) for lp, actions \
                                                 in zip(log_probs_list, train_batch['applicable_actions_list'])]))
        entropy_loss = -policy_entropy * self.curr_entropy_coeff

        loss = ppo_loss + entropy_loss + critic_loss # loss = actor_loss + critic_loss

        # ---- Accumulate metrics across all epochs and mini-batches ----
        self.num_samples += len(train_batch['states'])
        self.num_minibatches += 1
        self.critic_loss_sum += critic_loss.detach().item()
        self.ppo_loss_sum += ppo_loss.detach().item()
        self.entropy_loss_sum += entropy_loss.detach().item()
        self.policy_entropy_sum += policy_entropy.detach().item()
        self.approx_kl_sum += approx_kl
        self.clip_fraction_sum += clip_fraction

        return loss

    # ------------------------------------------------------------------
    # Callbacks
    # ------------------------------------------------------------------

    def get_gradient_norm(self):
        # Function to avoid code duplication
        def _calculate_norm(parameters):
            total = 0.0
            for p in parameters:
                if p.grad is not None:
                    param_norm = p.grad.data.norm(2)
                    total += param_norm.item() ** 2
            return total ** 0.5
        
        total_norm_actor = _calculate_norm(self.actor.parameters())
        total_norm_critic = _calculate_norm(self.critic.parameters())
        return total_norm_actor, total_norm_critic

    def on_after_backward(self):
        total_norm_actor, total_norm_critic = self.get_gradient_norm()
        self.total_norm_actor_sum += total_norm_actor
        self.total_norm_critic_sum += total_norm_critic

    def on_train_end(self):
        super().on_train_end()
        self.anneal_entropy_coeff()

        n = self.num_minibatches  # correct denominator for already-averaged losses
        if n > 0 and self.curr_logging_it.item() % self.hparams['log_period'] == 0:
            self.logger.experiment.add_scalars(
                'Gradient Norm',
                {'Actor': self.total_norm_actor_sum / n,
                 'Critic': self.total_norm_critic_sum / n},
                global_step=self.curr_logging_it.item(),
            )
            self.logger.experiment.add_scalar(
                'Critic Loss', self.critic_loss_sum / n,
                global_step=self.curr_logging_it.item(),
            )
            self.logger.experiment.add_scalars(
                'Actor Losses',
                {'PPO Loss': self.ppo_loss_sum / n,
                 'Entropy Loss': self.entropy_loss_sum / n},
                global_step=self.curr_logging_it.item(),
            )
            self.logger.experiment.add_scalar(
                'Policy Entropy', self.policy_entropy_sum / n,
                global_step=self.curr_logging_it.item(),
            )
            self.logger.experiment.add_scalar(
                'Approx KL', self.approx_kl_sum / n,
                global_step=self.curr_logging_it.item(),
            )
            self.logger.experiment.add_scalar(
                'Clip Fraction', self.clip_fraction_sum / n,
                global_step=self.curr_logging_it.item(),
            )

        # Reset counters
        self.total_norm_actor_sum = 0.0
        self.total_norm_critic_sum = 0.0
        self.critic_loss_sum = 0.0
        self.ppo_loss_sum = 0.0
        self.entropy_loss_sum = 0.0
        self.policy_entropy_sum = 0.0
        self.approx_kl_sum = 0.0
        self.clip_fraction_sum = 0.0
        self.num_samples = 0
        self.num_minibatches = 0
