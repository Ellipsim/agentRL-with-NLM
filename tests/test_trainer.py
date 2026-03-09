"""
> test_trainer.py

Tests for PolicyTrainer trajectory processing methods.

Tests the core logic of:
  - Return calculation (discounted cumulative rewards)
  - Advantage calculation (GAE)
  - Trajectory processing pipeline
  - Solving and collecting trajectories
"""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock
import torch
from argparse import Namespace


# =====================================================================
# Fixtures
# =====================================================================

@pytest.fixture
def mock_args():
    """Create mock args with trainer configuration"""
    return Namespace(
        disc_factor=0.99,
        gae_factor=0.95,
        solve_PPO_epochs=3,
        batch_size=32,
        grad_clip=0.5,
        min_samples_train=10,
        log_period=5,
        val_period=10,
        num_problems_train=5,
        num_problems_val=3,
        num_problems_test=3,
        max_actions_train=50,
        max_actions_val=50,
        max_actions_test=50,
    )


@pytest.fixture
def mock_policy():
    """Create mock policy that returns constant state values"""
    policy = Mock()
    
    def mock_state_values(internal_states):
        values = [torch.tensor(0.5) for _ in internal_states]
        return values, None
    
    policy.calculate_state_values = Mock(side_effect=mock_state_values)
    return policy


@pytest.fixture
def mock_problem_solver():
    """Create mock problem solver"""
    return Mock()


@pytest.fixture
def mock_device():
    """Create mock device"""
    return torch.device('cpu')


@pytest.fixture
def trainer(mock_args, mock_problem_solver, mock_policy, mock_device, tmp_path):
    """Create a minimal trainer for testing core methods"""
    
    class MinimalTrainer:
        """Minimal trainer with just the methods we test"""
        
        def __init__(self, args, device):
            self.args = args
            self.policy = mock_policy
            self.problem_solver = mock_problem_solver
            self.device = device
        
        def _calculate_return_trajectories(self, trajectories):
            """Calculate discounted returns for each sample."""
            for i in range(len(trajectories)):
                return_curr_state = 0
                
                for j in range(len(trajectories[i]) - 1, -1, -1):
                    reward = trajectories[i][j]['reward']
                    return_curr_state = reward + self.args.disc_factor * return_curr_state
                    
                    trajectories[i][j]['total_reward'] = reward
                    trajectories[i][j]['return'] = return_curr_state
        
        def _calculate_advantage_trajectories(self, policy, trajectories):
            """Calculate advantages using GAE."""
            for i in range(len(trajectories)):
                if len(trajectories[i]) > 0:
                    internal_states = [sample['internal_state'] for sample in trajectories[i]]
                    state_values, _ = policy.calculate_state_values(internal_states)
                    state_values = [v.item() for v in state_values]
                    
                    advantage_curr_state = trajectories[i][-1]['total_reward'] - state_values[-1]
                    trajectories[i][-1]['advantage'] = advantage_curr_state
                    trajectories[i][-1]['state_value'] = state_values[-1]
                    
                    for j in range(len(trajectories[i]) - 2, -1, -1):
                        delta_curr_state = (trajectories[i][j]['total_reward'] + 
                                           self.args.disc_factor * state_values[j + 1] - 
                                           state_values[j])
                        advantage_curr_state = (delta_curr_state + 
                                               (self.args.disc_factor * self.args.gae_factor) * 
                                               advantage_curr_state)
                        trajectories[i][j]['advantage'] = advantage_curr_state
                        trajectories[i][j]['state_value'] = state_values[j]
        
        def _process_trajectories(self, trajectories):
            """Process trajectories for training."""
            self._calculate_return_trajectories(trajectories)
            self._calculate_advantage_trajectories(self.policy, trajectories)
            
            samples = []
            for trajectory in trajectories:
                samples.extend(trajectory)
            
            return samples
        
        def _solve_and_collect_trajectories(self, problems, max_actions):
            """Solve problems and collect trajectories."""
            num_problems = len(problems)
            
            if num_problems == 0:
                return [], [], [], 0.0
            
            if isinstance(max_actions, int):
                max_actions_list = [max_actions] * num_problems
            else:
                assert len(max_actions) == num_problems
                max_actions_list = list(max_actions)
            
            is_solved, problem_info_list, trajectories, elapsed = self.problem_solver.solve_problems(
                problems,
                list_max_actions=max_actions_list
            )
            
            return is_solved, problem_info_list, trajectories, elapsed
    
    return MinimalTrainer(mock_args, mock_device)


# =====================================================================
# Tests: Return Calculation
# =====================================================================

class TestCalculateReturnTrajectories:
    """Test _calculate_return_trajectories method"""
    
    def test_single_step_trajectory(self, trainer):
        """Test return calculation for single-step trajectory"""
        trajectories = [[
            {'reward': 1.0}
        ]]
        
        trainer._calculate_return_trajectories(trajectories)
        
        assert trajectories[0][0]['total_reward'] == 1.0
        assert trajectories[0][0]['return'] == 1.0
    
    def test_multi_step_trajectory(self, trainer):
        """Test return calculation for multi-step trajectory with goal bonus"""
        trajectories = [[
            {'reward': -0.01},
            {'reward': -0.01},
            {'reward': 1.375},
        ]]
        
        trainer._calculate_return_trajectories(trajectories)
        
        gamma = trainer.args.disc_factor
        
        # R_2 = 1.375 (last step)
        assert abs(trajectories[0][2]['return'] - 1.375) < 0.001
        
        # R_1 = -0.01 + 0.99 * 1.375 = 1.351
        expected_r1 = -0.01 + gamma * 1.375
        assert abs(trajectories[0][1]['return'] - expected_r1) < 0.001
        
        # R_0 = -0.01 + 0.99 * R_1
        expected_r0 = -0.01 + gamma * expected_r1
        assert abs(trajectories[0][0]['return'] - expected_r0) < 0.001
    
    def test_multiple_trajectories(self, trainer):
        """Test return calculation for multiple trajectories"""
        trajectories = [
            [{'reward': 1.0}],
            [{'reward': -0.01}, {'reward': 0.5}],
            [{'reward': 0.0}, {'reward': 0.0}, {'reward': 1.0}],
        ]
        
        trainer._calculate_return_trajectories(trajectories)
        
        # Verify all trajectories have returns
        for traj in trajectories:
            for sample in traj:
                assert 'return' in sample
                assert 'total_reward' in sample
    
    def test_discount_factor_zero(self, trainer):
        """Test with discount factor = 0 (only immediate rewards)"""
        trainer.args.disc_factor = 0.0
        trajectories = [[
            {'reward': 1.0},
            {'reward': 2.0},
        ]]
        
        trainer._calculate_return_trajectories(trajectories)
        
        # With gamma=0, R_t = r_t
        assert trajectories[0][0]['return'] == 1.0
        assert trajectories[0][1]['return'] == 2.0
    
    def test_discount_factor_one(self, trainer):
        """Test with discount factor = 1 (all future rewards equal)"""
        trainer.args.disc_factor = 1.0
        trajectories = [[
            {'reward': 1.0},
            {'reward': 2.0},
        ]]
        
        trainer._calculate_return_trajectories(trajectories)
        
        # With gamma=1, sum all future rewards
        assert trajectories[0][0]['return'] == 3.0  # 1 + 2
        assert trajectories[0][1]['return'] == 2.0  # 2


# =====================================================================
# Tests: Advantage Calculation (GAE)
# =====================================================================

class TestCalculateAdvantageTrajectories:
    """Test _calculate_advantage_trajectories method (GAE)"""
    
    def test_single_step_trajectory(self, trainer, mock_policy):
        """Test advantage for single-step trajectory: A = R - V"""
        trajectories = [[
            {
                'reward': 1.0,
                'total_reward': 1.0,
                'return': 1.0,
                'internal_state': Mock(),
            }
        ]]
        
        # V(s) = 0.5, so A = 1.0 - 0.5 = 0.5
        trainer._calculate_advantage_trajectories(mock_policy, trajectories)
        
        assert abs(trajectories[0][0]['advantage'] - 0.5) < 0.001
        assert abs(trajectories[0][0]['state_value'] - 0.5) < 0.001
    
    def test_multi_step_gae(self, trainer, mock_policy):
        """Test GAE advantage formula: A_t = delta_t + (gamma*lambda)*A_{t+1}"""
        trajectories = [[
            {
                'total_reward': 0.0,
                'return': 1.0,
                'internal_state': Mock(),
            },
            {
                'total_reward': 1.0,
                'return': 1.0,
                'internal_state': Mock(),
            },
        ]]
        
        # Override mock to return specific values
        state_values = [torch.tensor(0.0), torch.tensor(1.0)]
        mock_policy.calculate_state_values = Mock(return_value=(state_values, None))
        
        trainer._calculate_advantage_trajectories(mock_policy, trajectories)
        
        # For last step: A = R - V = 1.0 - 1.0 = 0.0
        assert abs(trajectories[0][1]['advantage'] - 0.0) < 0.001
        
        # For first step: delta = r + gamma*V(s_1) - V(s_0)
        gamma = trainer.args.disc_factor
        lambda_gae = trainer.args.gae_factor
        delta = 0.0 + gamma * 1.0 - 0.0  # = 0.99
        expected_a0 = delta + (gamma * lambda_gae) * 0.0  # = 0.99
        
        assert abs(trajectories[0][0]['advantage'] - expected_a0) < 0.001
    
    def test_empty_trajectory_skipped(self, trainer, mock_policy):
        """Test that empty trajectories are skipped"""
        trajectories = [[], [{'total_reward': 1.0, 'return': 1.0, 'internal_state': Mock()}]]
        
        state_values = [torch.tensor(0.5)]
        mock_policy.calculate_state_values = Mock(return_value=(state_values, None))
        
        # Should not crash
        trainer._calculate_advantage_trajectories(mock_policy, trajectories)
        
        # Only second trajectory should have advantage
        assert 'advantage' not in trajectories[0]
        assert 'advantage' in trajectories[1][0]


# =====================================================================
# Tests: Process Trajectories Pipeline
# =====================================================================

class TestProcessTrajectories:
    """Test _process_trajectories method (full pipeline)"""
    
    def test_single_trajectory(self, trainer, mock_policy):
        """Test processing single trajectory"""
        trajectories = [[
            {
                'reward': -0.01,
                'internal_state': Mock(),
            },
            {
                'reward': 1.375,
                'internal_state': Mock(),
            },
        ]]
        
        state_values = [torch.tensor(0.5), torch.tensor(0.9)]
        mock_policy.calculate_state_values = Mock(return_value=(state_values, None))
        
        samples = trainer._process_trajectories(trajectories)
        
        # Should have 2 samples
        assert len(samples) == 2
        
        # All samples should have required fields
        for sample in samples:
            assert 'reward' in sample
            assert 'total_reward' in sample
            assert 'return' in sample
            assert 'advantage' in sample
            assert 'state_value' in sample
    
    def test_multiple_trajectories_flattened(self, trainer, mock_policy):
        """Test multiple trajectories are flattened to single list"""
        trajectories = [
            [{'reward': 1.0, 'internal_state': Mock()}, 
             {'reward': 2.0, 'internal_state': Mock()}],
            [{'reward': 3.0, 'internal_state': Mock()}],
        ]
        
        state_values = [torch.tensor(0.5), torch.tensor(0.5), torch.tensor(0.5)]
        mock_policy.calculate_state_values = Mock(return_value=(state_values, None))
        
        samples = trainer._process_trajectories(trajectories)
        
        # Should be flattened to 3 samples
        assert len(samples) == 3
        assert isinstance(samples, list)
        assert all(isinstance(s, dict) for s in samples)
    
    def test_returns_include_rewards(self, trainer, mock_policy):
        """Test that processed samples include original rewards"""
        trajectories = [[
            {'reward': -0.01, 'internal_state': Mock()},
            {'reward': 1.375, 'internal_state': Mock()},
        ]]
        
        state_values = [torch.tensor(0.0), torch.tensor(1.0)]
        mock_policy.calculate_state_values = Mock(return_value=(state_values, None))
        
        samples = trainer._process_trajectories(trajectories)
        
        # Original rewards should be preserved
        assert samples[0]['reward'] == -0.01
        assert samples[1]['reward'] == 1.375


# =====================================================================
# Tests: Solve and Collect Trajectories
# =====================================================================

class TestSolveAndCollectTrajectories:
    """Test _solve_and_collect_trajectories method"""
    
    def test_single_int_budget(self, trainer, mock_problem_solver):
        """Test solving with single int action budget"""
        problems = [Mock() for _ in range(3)]
        
        problem_info = [
            {'goal_reached': True, 'num_steps': 10, 'efficiency': 0.8},
            {'goal_reached': False, 'num_steps': 50, 'efficiency': 0.0},
            {'goal_reached': True, 'num_steps': 15, 'efficiency': 0.7},
        ]
        trajectories = [
            [{'reward': 1.0}],
            [{'reward': -0.01}],
            [{'reward': 1.0}],
        ]
        is_solved = [True, False, True]
        
        mock_problem_solver.solve_problems = Mock(
            return_value=(is_solved, problem_info, trajectories, 1.5)
        )
        
        is_solved_ret, info_ret, traj_ret, elapsed_ret = trainer._solve_and_collect_trajectories(
            problems,
            max_actions=50
        )
        
        # Verify solver was called with correct budget
        call_args = mock_problem_solver.solve_problems.call_args
        assert call_args[1]['list_max_actions'] == [50, 50, 50]
        
        # Verify returns
        assert is_solved_ret == is_solved
        assert info_ret == problem_info
        assert traj_ret == trajectories
        assert elapsed_ret == 1.5
    
    def test_tuple_per_problem_budget(self, trainer, mock_problem_solver):
        """Test solving with per-problem action budget tuple"""
        problems = [Mock() for _ in range(3)]
        
        problem_info = [
            {'goal_reached': True, 'num_steps': 5, 'efficiency': 0.9},
            {'goal_reached': True, 'num_steps': 20, 'efficiency': 0.6},
            {'goal_reached': True, 'num_steps': 15, 'efficiency': 0.7},
        ]
        trajectories = [[{'reward': 1.0}] for _ in range(3)]
        is_solved = [True, True, True]
        
        mock_problem_solver.solve_problems = Mock(
            return_value=(is_solved, problem_info, trajectories, 1.0)
        )
        
        is_solved_ret, info_ret, traj_ret, elapsed_ret = trainer._solve_and_collect_trajectories(
            problems,
            max_actions=(10, 30, 20)
        )
        
        # Verify each problem got its own budget
        call_args = mock_problem_solver.solve_problems.call_args
        assert call_args[1]['list_max_actions'] == [10, 30, 20]
    
    def test_tuple_length_mismatch_error(self, trainer):
        """Test that mismatched tuple length raises AssertionError"""
        problems = [Mock() for _ in range(3)]
        
        with pytest.raises(AssertionError):
            trainer._solve_and_collect_trajectories(
                problems,
                max_actions=(10, 20)  # Only 2, but 3 problems
            )
    
    def test_empty_problems_returns_empty(self, trainer):
        """Test with empty problems list"""
        is_solved, info, traj, elapsed = trainer._solve_and_collect_trajectories(
            [],
            max_actions=50
        )
        
        assert is_solved == []
        assert info == []
        assert traj == []
        assert elapsed == 0.0
    
    def test_success_and_failure_mix(self, trainer, mock_problem_solver):
        """Test problems with mixed success/failure"""
        problems = [Mock() for _ in range(4)]
        
        is_solved = [True, True, False, False]
        problem_info = [
            {'goal_reached': True, 'num_steps': 10},
            {'goal_reached': True, 'num_steps': 15},
            {'goal_reached': False, 'num_steps': 50},
            {'goal_reached': False, 'num_steps': 50},
        ]
        trajectories = [[{'reward': 1.0}] for _ in range(4)]
        
        mock_problem_solver.solve_problems = Mock(
            return_value=(is_solved, problem_info, trajectories, 2.0)
        )
        
        is_solved_ret, info_ret, _, _ = trainer._solve_and_collect_trajectories(
            problems,
            max_actions=50
        )
        
        # Verify mixed results
        assert sum(is_solved_ret) == 2  # 2 successes
        assert sum(1 for p in info_ret if p['goal_reached']) == 2


# =====================================================================
# Edge Case Tests
# =====================================================================

class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_very_long_trajectory(self, trainer, mock_policy):
        """Test with very long trajectory (1000 steps)"""
        trajectory = [
            {'reward': -0.01, 'internal_state': Mock()}
            for _ in range(1000)
        ]
        trajectory[-1]['reward'] = 1.0  # Goal at end
        
        state_values = [torch.tensor(0.0) for _ in range(1000)]
        mock_policy.calculate_state_values = Mock(return_value=(state_values, None))
        
        trajectories = [trajectory]
        samples = trainer._process_trajectories(trajectories)
        
        assert len(samples) == 1000
        assert all('advantage' in s for s in samples)
    
    def test_all_zero_rewards(self, trainer, mock_policy):
        """Test trajectory with all zero rewards"""
        trajectories = [[
            {'reward': 0.0, 'internal_state': Mock()},
            {'reward': 0.0, 'internal_state': Mock()},
        ]]
        
        state_values = [torch.tensor(0.0), torch.tensor(0.0)]
        mock_policy.calculate_state_values = Mock(return_value=(state_values, None))
        
        samples = trainer._process_trajectories(trajectories)
        
        assert len(samples) == 2
        assert all(s['return'] == 0.0 for s in samples)
        assert all(s['advantage'] == 0.0 for s in samples)
    
    def test_negative_advantages(self, trainer, mock_policy):
        """Test that advantages can be negative (worse than baseline)"""
        trajectories = [[
            {
                'total_reward': -1.0,  # Bad action
                'return': -1.0,
                'internal_state': Mock(),
            }
        ]]
        
        state_values = [torch.tensor(0.5)]  # Predicted value better than actual
        mock_policy.calculate_state_values = Mock(return_value=(state_values, None))
        
        trainer._calculate_advantage_trajectories(mock_policy, trajectories)
        
        # A = R - V = -1.0 - 0.5 = -1.5
        assert trajectories[0][0]['advantage'] < 0


# =====================================================================
# Data Format Tests
# =====================================================================

class TestDataFormats:
    """Test that outputs match expected data formats for solver_collate_fn"""
    
    def test_sample_dict_structure(self, trainer, mock_policy):
        """Test that processed samples have all fields needed by solver_collate_fn"""
        trajectories = [[
            {
                'reward': -0.01,
                'state': Mock(),
                'internal_state': Mock(),
                'applicable_actions': tuple(),
                'chosen_action': Mock(),
                'chosen_action_ind': 0,
                'action_log_prob': -2.3,
            }
        ]]
        
        state_values = [torch.tensor(0.5)]
        mock_policy.calculate_state_values = Mock(return_value=(state_values, None))
        
        samples = trainer._process_trajectories(trajectories)
        
        # Check all solver_collate_fn expected fields
        required_fields = [
            'state', 'internal_state', 'applicable_actions',
            'chosen_action', 'chosen_action_ind', 'action_log_prob',
            'reward', 'return', 'advantage', 'state_value'
        ]
        
        for field in required_fields:
            assert field in samples[0], f"Missing field: {field}"
    
    def test_numeric_types(self, trainer, mock_policy):
        """Test that numeric fields have correct types"""
        trajectories = [[
            {'reward': -0.01, 'internal_state': Mock()}
        ]]
        
        state_values = [torch.tensor(0.5)]
        mock_policy.calculate_state_values = Mock(return_value=(state_values, None))
        
        samples = trainer._process_trajectories(trajectories)
        sample = samples[0]
        
        # Check types
        assert isinstance(sample['reward'], float)
        assert isinstance(sample['return'], (int, float))
        assert isinstance(sample['advantage'], (int, float))
        assert isinstance(sample['state_value'], (int, float))