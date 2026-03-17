"""
Tests for src/agent/controller/trainer.py

Covers:
- train_one_step runs without error
- Checkpoint saving/loading
- Periodic test evaluation triggers correctly
- Replay buffer save/load
- PPO update with minimal samples
"""

import pytest
import torch
import json
import argparse
from pathlib import Path
from unittest.mock import MagicMock, patch
import tempfile

from src.agent.controller.trainer import PolicyTrainer, ReplayBuffer


# =====================================================================
# Fixtures
# =====================================================================

@pytest.fixture
def minimal_args():
    """Minimal args namespace for PolicyTrainer."""
    return argparse.Namespace(
        max_actions_train=20,
        max_actions_test=20,
        batch_size=8,
        min_samples_train=2,
        disc_factor=0.99,
        gae_factor=0.95,
        grad_clip=0.5,
        log_period=1,
        test_period=5,
        solve_PPO_epochs=1,
        device='cpu',
        seed=1,
        steps=10,
        num_problems_test=5,
    )


@pytest.fixture
def mock_policy():
    """A mock policy that returns dummy tensors."""
    policy = MagicMock()
    policy.curr_logging_it = 0
    policy.hparams = {}

    # calculate_state_values returns (list of tensors, list of internal states)
    policy.calculate_state_values = MagicMock(
        return_value=([torch.tensor(0.5) for _ in range(10)], [None] * 10)
    )
    # named_parameters and named_buffers for save_checkpoint
    policy.named_parameters = MagicMock(return_value=[])
    policy.named_buffers = MagicMock(return_value=[])
    policy.state_dict = MagicMock(return_value={})
    policy.to = MagicMock(return_value=policy)

    return policy


@pytest.fixture
def mock_problem_solver():
    """A mock ProblemSolver that returns dummy trajectories."""
    solver = MagicMock()

    def fake_solve(problems, list_max_actions):
        num = len(problems)
        is_solved = [True] * num
        problem_info = [
            {'goal_reached': True, 'efficiency': 0.8, 'num_steps': 5,
             'max_actions': 20, 'truncated': False, 'success': True,
             'solution_ratio': 0.25, 'action_history': [], 'num_objects': {},
             'num_goal_atoms': 2}
            for _ in range(num)
        ]
        # Each trajectory has 5 samples
        trajectories = [
            [
                {
                    'state': MagicMock(),
                    'internal_state': MagicMock(),
                    'applicable_actions': [],
                    'chosen_action': None,
                    'chosen_action_ind': 0,
                    'action_log_prob': torch.tensor(-1.0),
                    'reward': 0.1,
                }
                for _ in range(5)
            ]
            for _ in range(num)
        ]
        return is_solved, problem_info, trajectories, 0.1

    solver.solve_problems = MagicMock(side_effect=fake_solve)
    return solver


@pytest.fixture
def trainer(tmp_path, minimal_args, mock_policy, mock_problem_solver):
    """A PolicyTrainer with mocked dependencies."""
    return PolicyTrainer(
        args=minimal_args,
        experiment_folder_path=tmp_path,
        problem_solver=mock_problem_solver,
        policy=mock_policy,
        device=torch.device('cpu'),
    )


@pytest.fixture
def dummy_problems():
    """A list of mock PDDLProblem objects."""
    return [MagicMock() for _ in range(4)]


# =====================================================================
# Replay Buffer Tests
# =====================================================================

class TestReplayBuffer:

    def test_add_and_sample(self, tmp_path):
        buf = ReplayBuffer(max_size=10)
        buf.add('path/to/problem_1.pddl')
        buf.add('path/to/problem_2.pddl')
        assert len(buf) == 2
        sample = buf.sample()
        assert sample in ['path/to/problem_1.pddl', 'path/to/problem_2.pddl']

    def test_fifo_eviction(self, tmp_path):
        buf = ReplayBuffer(max_size=3)
        for i in range(5):
            buf.add(f'problem_{i}.pddl')
        assert len(buf) == 3
        assert 'problem_0.pddl' not in buf._paths
        assert 'problem_4.pddl' in buf._paths

    def test_no_duplicates(self):
        buf = ReplayBuffer(max_size=10)
        buf.add('problem_1.pddl')
        buf.add('problem_1.pddl')
        assert len(buf) == 1

    def test_save_and_load(self, tmp_path):
        buf = ReplayBuffer(max_size=10)
        buf.add('problem_1.pddl')
        buf.add('problem_2.pddl')
        buf.save(tmp_path)

        buf2 = ReplayBuffer(max_size=10)
        buf2.load(tmp_path)
        assert buf2._paths == buf._paths

    def test_register_dir(self, tmp_path):
        # Create dummy pddl files
        (tmp_path / 'p1.pddl').write_text('dummy')
        (tmp_path / 'p2.pddl').write_text('dummy')

        buf = ReplayBuffer(max_size=10)
        buf.register_dir(str(tmp_path))
        assert len(buf) == 2

    def test_sample_empty_returns_none(self):
        buf = ReplayBuffer(max_size=10)
        assert buf.sample() is None


# =====================================================================
# PolicyTrainer Tests
# =====================================================================

class TestPolicyTrainer:

    def test_train_one_step_runs(self, trainer, dummy_problems):
        """train_one_step completes without error and returns a dict."""
        with patch.object(trainer, '_perform_train_step'):
            metrics = trainer.train_one_step(
                problems=dummy_problems,
                test_problems=dummy_problems,
                current_step=1,
            )
        assert isinstance(metrics, dict)

    def test_train_one_step_skips_ppo_below_min_samples(self, trainer, minimal_args):
        """PPO is skipped when samples < min_samples_train."""
        minimal_args.min_samples_train = 1000
        with patch('src.agent.controller.trainer.pl.Trainer') as mock_pl_trainer:
            trainer.train_one_step(
                problems=[MagicMock()],
                test_problems=[],
                current_step=1,
            )
        # pl.Trainer.fit should never have been called
        mock_pl_trainer.return_value.fit.assert_not_called()

    def test_periodic_test_evaluation_triggers(self, trainer, dummy_problems, minimal_args):
        """Test evaluation runs when current_step % test_period == 0."""
        minimal_args.test_period = 5
        with patch.object(trainer, '_perform_train_step'):
            metrics = trainer.train_one_step(
                problems=dummy_problems,
                test_problems=dummy_problems,
                current_step=5,
            )
        assert 'test' in metrics

    def test_periodic_test_evaluation_does_not_trigger(self, trainer, dummy_problems, minimal_args):
        minimal_args.test_period = 5
        with patch.object(PolicyTrainer, '_perform_train_step'):
            metrics = trainer.train_one_step(
                problems=dummy_problems,
                test_problems=dummy_problems,
                current_step=3,
            )
        assert 'test' not in metrics

    # def test_periodic_test_evaluation_does_not_trigger(self, trainer, dummy_problems, minimal_args):
    #     """Test evaluation does not run on non-test steps."""
    #     minimal_args.test_period = 5
    #     metrics = trainer.train_one_step(
    #         problems=dummy_problems,
    #         test_problems=dummy_problems,
    #         current_step=3,
    #     )
    #     assert 'test' not in metrics

    def test_checkpoint_save_and_load(self, trainer, tmp_path, mock_policy):
        """Checkpoint is saved and can be loaded back."""
        mock_policy.named_parameters = MagicMock(
            return_value=[('weight', torch.tensor([1.0, 2.0]))]
        )
        mock_policy.named_buffers = MagicMock(return_value=[])

        ckpt_path = tmp_path / 'checkpoints' / 'last.ckpt'
        trainer.save_checkpoint(mock_policy, ckpt_path)

        assert ckpt_path.exists()
        loaded = torch.load(str(ckpt_path))
        assert 'state_dict' in loaded
        assert 'weight' in loaded['state_dict']

    def test_save_policy_creates_last_ckpt(self, trainer, tmp_path, mock_policy):
        """save_policy creates last.ckpt."""
        mock_policy.named_parameters = MagicMock(return_value=[])
        mock_policy.named_buffers = MagicMock(return_value=[])
        trainer.save_policy(save_best=False)
        assert (tmp_path / 'checkpoints' / 'last.ckpt').exists()

    def test_save_policy_creates_best_ckpt(self, trainer, tmp_path, mock_policy):
        """save_policy creates best.ckpt when save_best=True."""
        mock_policy.named_parameters = MagicMock(return_value=[])
        mock_policy.named_buffers = MagicMock(return_value=[])
        trainer.save_policy(save_best=True)
        assert (tmp_path / 'checkpoints' / 'best.ckpt').exists()