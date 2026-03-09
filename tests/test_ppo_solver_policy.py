"""
> test_ppo_solver_policy.py

Tests for PPOSolverPolicy - trained policy using PPO algorithm.
Runs on all .pddl files discovered in data/problems/

Run with:
    pytest tests/test_ppo_solver_policy.py -v
    pytest -m ppo -v
"""

import pytest
import torch
import argparse
from copy import deepcopy

from src.agent.pddl.pddl_problem import PDDLProblem
from src.agent.learning.generative_policy import PPOSolverPolicy, RandomPolicy
from src.agent.learning.model_wrapper import NLMWrapperActor, NLMWrapperCritic


@pytest.fixture
def mock_args():
    """Create mock arguments for PPOSolverPolicy."""
    return argparse.Namespace(
        solve_lr=1e-3,
        solve_PPO_epochs=1,
        solve_epsilon=0.2,
        solve_entropy_coeffs=0.01,
        solve_lifted_entropy_weight=0.5,
        critic_loss_weight=0.5,
        weight_decay=0.0,
        log_period=10,
        # NLM hyperparameters
        breadth=3,
        depth=5,
        hidden_features=8,
        mlp_hidden_features=0,
        residual="input",
        exclude_self=True,
        use_batch_norm=False,
        activation='sigmoid',
        input_max_size=True,
        input_num_actions=True,
        input_num_objs=True,
        input_num_atoms=True,
    )


@pytest.fixture
def dummy_pddl_state(parser):
    """Create dummy PDDL state with domain actions as predicates."""
    from src.agent.pddl.pddl_state import PDDLState
    
    # Convert domain actions to predicate format
    # Each action becomes a predicate with the same arity as its parameters
    domain_actions = set([
        (action[0], tuple([var for var, var_class in zip(action[1][0], action[1][1]) if var_class=='param']))
        for action in parser.actions
    ])
    
    # Create state with actions as predicates
    # NOTE: PDDL dummy state actions are encoded as predicates (legacy NeSIG)
    dummy_state = PDDLState(
        types=parser.types,
        type_hierarchy=parser.type_hierarchy,
        predicates=domain_actions,  # ← Actions treated as predicates!
        objects=[],
        atoms=set()
    )
    return dummy_state


@pytest.fixture
def device():
    """Get device (CPU for testing)."""
    return torch.device("cpu")


@pytest.mark.ppo
class TestRandomPolicy:
    """Tests for RandomPolicy baseline."""

    def test_random_policy_initializes(self):
        """Test that RandomPolicy initializes correctly."""
        policy = RandomPolicy()
        assert policy is not None

    def test_random_policy_forward_shape(self, parser, problem_file):
        """Test that forward() returns correct shapes."""
        policy = RandomPolicy()
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=50)
        applicable = problem.applicable_ground_actions()
        
        log_probs_list, internal_states = policy.forward(
            [problem],
            [applicable]
        )
        
        assert len(log_probs_list) == 1
        assert len(internal_states) == 1
        assert log_probs_list[0].shape[0] == len(applicable)

    def test_random_policy_log_probs_sum_to_one(self, parser, problem_file):
        """Test that log-probs correspond to uniform distribution."""
        policy = RandomPolicy()
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=50)
        applicable = problem.applicable_ground_actions()
        
        log_probs_list, _ = policy.forward([problem], [applicable])
        log_probs = log_probs_list[0]
        
        # exp(log_probs) should sum to ~1 (uniform distribution)
        probs = torch.exp(log_probs)
        assert torch.allclose(probs.sum(), torch.tensor(1.0), atol=1e-6)

    def test_random_policy_select_actions_returns_valid_action(self, parser, problem_file):
        """Test that select_actions returns a valid applicable action."""
        policy = RandomPolicy()
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=50)
        applicable = problem.applicable_ground_actions()
        
        chosen_actions, chosen_log_probs, internal_states = policy.select_actions(
            [problem],
            [applicable]
        )
        
        assert len(chosen_actions) == 1
        assert chosen_actions[0] in applicable
        assert len(chosen_log_probs) == 1

    def test_random_policy_no_training(self):
        """Test that RandomPolicy raises error on training_step."""
        policy = RandomPolicy()
        with pytest.raises(NotImplementedError):
            policy.training_step({})

    def test_random_policy_multiple_problems(self, fresh_parser, problem_file):
        """Test RandomPolicy with multiple problems."""
        from copy import deepcopy
        policy = RandomPolicy()
        
        problem1 = PDDLProblem.load_from_pddl(fresh_parser(), problem_file, max_actions=50)
        problem2 = PDDLProblem.load_from_pddl(fresh_parser(), problem_file, max_actions=50)
        
        applicable1 = problem1.applicable_ground_actions()
        applicable2 = problem2.applicable_ground_actions()
        
        chosen_actions, _, _ = policy.select_actions(
            [problem1, problem2],
            [applicable1, applicable2]
        )
        
        assert len(chosen_actions) == 2
        assert chosen_actions[0] in applicable1
        assert chosen_actions[1] in applicable2


@pytest.mark.ppo
class TestPPOPolicyInitialization:
    """Tests for PPOSolverPolicy initialization."""

    def test_ppo_policy_initializes(self, mock_args, dummy_pddl_state, device):
        """Test that PPOSolverPolicy initializes correctly."""
        actor_args = {"dummy_pddl_state": dummy_pddl_state}
        critic_args = {"dummy_pddl_state": dummy_pddl_state}
        
        policy = PPOSolverPolicy(
            mock_args,
            NLMWrapperActor,
            actor_args,
            NLMWrapperCritic,
            critic_args,
            device,
        )
        
        assert policy is not None
        assert policy.actor is not None
        assert policy.critic is not None

    def test_ppo_policy_has_hparams(self, mock_args, dummy_pddl_state, device):
        """Test that PPOSolverPolicy saves hyperparameters."""
        actor_args = {"dummy_pddl_state": dummy_pddl_state}
        critic_args = {"dummy_pddl_state": dummy_pddl_state}
        
        policy = PPOSolverPolicy(
            mock_args,
            NLMWrapperActor,
            actor_args,
            NLMWrapperCritic,
            critic_args,
            device,
        )
        
        assert policy.hparams['solve_lr'] == mock_args.solve_lr
        assert policy.hparams['solve_epsilon'] == mock_args.solve_epsilon

    def test_ppo_policy_entropy_coeffs_single_value(self, mock_args, dummy_pddl_state, device):
        """Test entropy coefficient handling with single float."""
        args = deepcopy(mock_args)
        args.solve_entropy_coeffs = 0.01
        
        actor_args = {"dummy_pddl_state": dummy_pddl_state}
        critic_args = {"dummy_pddl_state": dummy_pddl_state}
        
        policy = PPOSolverPolicy(
            args,
            NLMWrapperActor,
            actor_args,
            NLMWrapperCritic,
            critic_args,
            device,
        )
        
        assert torch.allclose(policy.curr_entropy_coeff, torch.tensor(0.01, dtype=torch.float32))

    def test_ppo_policy_entropy_coeffs_tuple(self, mock_args, dummy_pddl_state, device):
        """Test entropy coefficient handling with annealing tuple."""
        args = deepcopy(mock_args)
        args.solve_entropy_coeffs = (0.1, 0.01, 100)  # (init, final, n_iters)
        
        actor_args = {"dummy_pddl_state": dummy_pddl_state}
        critic_args = {"dummy_pddl_state": dummy_pddl_state}
        
        policy = PPOSolverPolicy(
            args,
            NLMWrapperActor,
            actor_args,
            NLMWrapperCritic,
            critic_args,
            device,
        )
        
        assert torch.allclose(policy.curr_entropy_coeff, torch.tensor(0.1, dtype=torch.float32))
        assert policy.final_entropy_coeff == 0.01


@pytest.mark.ppo
class TestPPOPolicyForward:
    """Tests for PPOSolverPolicy forward pass."""

    def test_ppo_forward_returns_log_probs_and_states(self, mock_args, fresh_parser, problem_file, dummy_pddl_state, device):
        """Test that forward() returns log-probs and internal states."""
        actor_args = {"dummy_pddl_state": dummy_pddl_state}
        critic_args = {"dummy_pddl_state": dummy_pddl_state}
        
        policy = PPOSolverPolicy(
            mock_args,
            NLMWrapperActor,
            actor_args,
            NLMWrapperCritic,
            critic_args,
            device,
        )
        
        problem = PDDLProblem.load_from_pddl(fresh_parser(), problem_file, max_actions=50)
        applicable = problem.applicable_ground_actions()
        
        log_probs_list, internal_states = policy.forward([problem], [applicable])
        
        assert len(log_probs_list) == 1
        assert len(internal_states) == 1
        assert log_probs_list[0].shape[0] == len(applicable)

    def test_ppo_select_actions_samples_correctly(self, mock_args, fresh_parser, problem_file, dummy_pddl_state, device):
        """Test that select_actions samples valid actions."""
        actor_args = {"dummy_pddl_state": dummy_pddl_state}
        critic_args = {"dummy_pddl_state": dummy_pddl_state}
        
        policy = PPOSolverPolicy(
            mock_args,
            NLMWrapperActor,
            actor_args,
            NLMWrapperCritic,
            critic_args,
            device,
        )
        
        problem = PDDLProblem.load_from_pddl(fresh_parser(), problem_file, max_actions=50)
        applicable = problem.applicable_ground_actions()
        
        chosen_actions, chosen_log_probs, _ = policy.select_actions([problem], [applicable])
        
        assert len(chosen_actions) == 1
        assert chosen_actions[0] in applicable
        assert len(chosen_log_probs) == 1


@pytest.mark.ppo
class TestPPOPolicyCritic:
    """Tests for PPOSolverPolicy critic."""

    def test_critic_returns_state_values(self, mock_args, fresh_parser, problem_file, dummy_pddl_state, device):
        """Test that critic returns state values."""
        actor_args = {"dummy_pddl_state": dummy_pddl_state}
        critic_args = {"dummy_pddl_state": dummy_pddl_state}
        
        policy = PPOSolverPolicy(
            mock_args,
            NLMWrapperActor,
            actor_args,
            NLMWrapperCritic,
            critic_args,
            device,
        )
        
        problem = PDDLProblem.load_from_pddl(fresh_parser(), problem_file, max_actions=50)
        
        state_values, internal_states = policy.calculate_state_values([problem])
        
        assert len(state_values) == 1
        assert isinstance(state_values[0], torch.Tensor)
        assert state_values[0].shape == torch.Size([])  # Scalar


@pytest.mark.ppo
class TestPPOPolicyEntropy:
    """Tests for PPOSolverPolicy entropy calculation."""

    def test_entropy_single_action_returns_zero(self, mock_args, parser, problem_file, dummy_pddl_state, device):
        """Test that entropy is zero with single action."""
        actor_args = {"dummy_pddl_state": dummy_pddl_state}
        critic_args = {"dummy_pddl_state": dummy_pddl_state}
        
        policy = PPOSolverPolicy(
            mock_args,
            NLMWrapperActor,
            actor_args,
            NLMWrapperCritic,
            critic_args,
            device,
        )
        
        log_probs = torch.tensor([0.0])  # Single action, log-prob = 0
        applicable_actions = [("stack", (0, 1))]
        
        entropy = policy.calculate_entropy(log_probs, applicable_actions)
        
        assert entropy == 0.0 or torch.allclose(entropy, torch.tensor(0.0))

    def test_entropy_uniform_distribution_high(self, mock_args, parser, problem_file, dummy_pddl_state, device):
        """Test that entropy is high for uniform distribution."""
        actor_args = {"dummy_pddl_state": dummy_pddl_state}
        critic_args = {"dummy_pddl_state": dummy_pddl_state}
        
        policy = PPOSolverPolicy(
            mock_args,
            NLMWrapperActor,
            actor_args,
            NLMWrapperCritic,
            critic_args,
            device,
        )
        
        # Uniform distribution over 4 actions
        log_probs = torch.log(torch.ones(4) / 4)
        applicable_actions = [
            ("stack", (0, 1)),
            ("stack", (1, 0)),
            ("unstack", (0,)),
            ("pick", (1,)),
        ]
        
        entropy = policy.calculate_entropy(log_probs, applicable_actions)
        
        # Entropy should be positive and non-zero
        assert entropy > 0.0

    def test_entropy_annealing(self, mock_args, dummy_pddl_state, device):
        """Test that entropy coefficient anneals correctly."""
        args = deepcopy(mock_args)
        args.solve_entropy_coeffs = (0.1, 0.01, 10)
        
        actor_args = {"dummy_pddl_state": dummy_pddl_state}
        critic_args = {"dummy_pddl_state": dummy_pddl_state}
        
        policy = PPOSolverPolicy(
            args,
            NLMWrapperActor,
            actor_args,
            NLMWrapperCritic,
            critic_args,
            device,
        )
        
        initial_coeff = policy.curr_entropy_coeff.item()
        policy.anneal_entropy_coeff()
        after_anneal = policy.curr_entropy_coeff.item()
        
        # Should decrease (with tolerance for floating point errors)
        assert after_anneal <= initial_coeff + 1e-6


@pytest.mark.ppo
class TestPPOPolicyOptimizer:
    """Tests for PPOSolverPolicy optimizer configuration."""

    def test_configure_optimizers_returns_adamw(self, mock_args, dummy_pddl_state, device):
        """Test that configure_optimizers returns AdamW optimizer."""
        actor_args = {"dummy_pddl_state": dummy_pddl_state}
        critic_args = {"dummy_pddl_state": dummy_pddl_state}
        
        policy = PPOSolverPolicy(
            mock_args,
            NLMWrapperActor,
            actor_args,
            NLMWrapperCritic,
            critic_args,
            device,
        )
        
        optimizer = policy.configure_optimizers()
        
        assert isinstance(optimizer, torch.optim.AdamW)

    def test_optimizer_has_correct_lr(self, mock_args, dummy_pddl_state, device):
        """Test that optimizer has correct learning rate."""
        actor_args = {"dummy_pddl_state": dummy_pddl_state}
        critic_args = {"dummy_pddl_state": dummy_pddl_state}
        
        policy = PPOSolverPolicy(
            mock_args,
            NLMWrapperActor,
            actor_args,
            NLMWrapperCritic,
            critic_args,
            device,
        )
        
        optimizer = policy.configure_optimizers()
        
        assert optimizer.param_groups[0]['lr'] == mock_args.solve_lr


@pytest.mark.ppo
class TestPPOPolicyGradientNorm:
    """Tests for PPOSolverPolicy gradient norm calculation."""

    def test_gradient_norm_returns_two_values(self, mock_args, dummy_pddl_state, device):
        """Test that get_gradient_norm returns actor and critic norms."""
        actor_args = {"dummy_pddl_state": dummy_pddl_state}
        critic_args = {"dummy_pddl_state": dummy_pddl_state}
        
        policy = PPOSolverPolicy(
            mock_args,
            NLMWrapperActor,
            actor_args,
            NLMWrapperCritic,
            critic_args,
            device,
        )
        
        actor_norm, critic_norm = policy.get_gradient_norm()
        
        assert isinstance(actor_norm, float)
        assert isinstance(critic_norm, float)

    def test_gradient_norm_zero_without_gradients(self, mock_args, dummy_pddl_state, device):
        """Test that gradient norms are zero before backward pass."""
        actor_args = {"dummy_pddl_state": dummy_pddl_state}
        critic_args = {"dummy_pddl_state": dummy_pddl_state}
        
        policy = PPOSolverPolicy(
            mock_args,
            NLMWrapperActor,
            actor_args,
            NLMWrapperCritic,
            critic_args,
            device,
        )
        
        actor_norm, critic_norm = policy.get_gradient_norm()
        
        # Should be 0 or very close to 0 (no gradients computed yet)
        assert actor_norm == 0.0 or actor_norm < 1e-6
        assert critic_norm == 0.0 or critic_norm < 1e-6