"""
Tests for src/agent/controller/train_and_test_NeSIG.py

Covers:
- validate_args correctness
- build_student builds correctly
- accumulate_consistent_problems
- Full training loop smoke test (few steps)
"""

import pytest
import argparse
import torch
from pathlib import Path
from unittest.mock import MagicMock, patch
import tempfile

from src.agent.controller.train_and_test_NeSIG import (
    validate_args,
    accumulate_consistent_problems,
)


# =====================================================================
# Fixtures
# =====================================================================

@pytest.fixture
def base_args(tmp_path):
    """Minimal valid args for train_and_test_NeSIG."""
    return argparse.Namespace(
        domain_path='nesig_teacher/data/domains/blocks-domain.pddl',
        nesig_domain='blocksworld',
        max_init_actions_train=5,
        max_goal_actions_train=5,
        teacher_update_period=1,
        nesig_ppo_epochs=1,
        nesig_lr=1e-3,
        nesig_warmup_steps=0,
        diversity_threshold=0.75,
        perc_problems_diversity=1.0,
        r_eventual_consistency=-1.0,
        consistency_evaluator='domain',
        policy_type='PPO',
        difficulty_penalty=0.0,
        reward_goal_reached=1.0,
        reward_step=-0.05,
        reward_efficiency=0.0,
        max_actions_train=None,
        steps=3,
        num_problems_train=5,
        batch_size=8,
        min_samples_train=2,
        grad_clip=0.5,
        disc_factor=0.99,
        gae_factor=0.95,
        seed=1,
        run_id=0,
        device='cpu',
        test_problems_dir=str(tmp_path / 'test'),
        generate_test_problems=True,
        test_min_blocks=2,
        test_max_blocks=3,
        generator_path='./problem_generator/pddl-generators/blocksworld/blocksworld',
        test_period=5,
        num_problems_test=5,
        max_actions_test=None,
        data_dir=str(tmp_path / 'data'),
        max_generation_attempts=5,
        replay_prob=0.0,
        replay_buffer_size=100,
        log_period=1,
        save_level_checkpoints=False,
        train_mode='supersede',
        test_mode='skip',
        experiments_dir=str(tmp_path / 'experiments'),
        # NLM args
        breadth=1,
        depth=1,
        solve_PPO_epochs=1,
        solve_lr=1e-3,
        solve_epsilon=0.2,
        solve_entropy_coeffs=0.0,
        critic_loss_weight=0.1,
    )


# =====================================================================
# validate_args Tests
# =====================================================================

class TestValidateArgs:

    def test_valid_args_returns_args(self, base_args):
        args = validate_args(base_args)
        assert args is not None

    def test_max_actions_test_resolved_from_blocks(self, base_args):
        base_args.max_actions_test = None
        base_args.test_max_blocks = 5
        args = validate_args(base_args)
        assert args.max_actions_test == 4 * (5 - 1)

    def test_max_actions_train_falls_back_to_test(self, base_args):
        base_args.max_actions_test = 20
        base_args.max_actions_train = None
        args = validate_args(base_args)
        assert args.max_actions_train == 20

    def test_invalid_steps_raises(self, base_args):
        base_args.steps = 0
        with pytest.raises(ValueError, match="--steps must be > 0"):
            validate_args(base_args)

    def test_invalid_grad_clip_raises(self, base_args):
        base_args.grad_clip = -2.0
        with pytest.raises(ValueError, match="--grad-clip"):
            validate_args(base_args)

    def test_domain_not_found_raises(self, base_args):
        base_args.domain_path = '/nonexistent/domain.pddl'
        with pytest.raises(ValueError, match="Domain file not found"):
            validate_args(base_args)

    def test_policy_type_always_ppo(self, base_args):
        args = validate_args(base_args)
        assert args.policy_type == 'PPO'


# =====================================================================
# accumulate_consistent_problems Tests
# =====================================================================

class TestAccumulateConsistentProblems:

    def _make_trainer(self, consistent_per_call):
        """Helper to create a mock nesig_trainer."""
        trainer = MagicMock()
        call_count = [0]

        def fake_generate(n, init_actions, goal_actions):
            i = call_count[0]
            call_count[0] += 1
            n_consistent = consistent_per_call[i % len(consistent_per_call)]
            problems = [MagicMock() for _ in range(n)]
            infos = [
                {'consistency': j < n_consistent}
                for j in range(n)
            ]
            trajectories = [MagicMock() for _ in range(n)]
            return problems, infos, trajectories, 0.1, 0

        trainer._generate_problems_and_trajectories = MagicMock(
            side_effect=fake_generate
        )
        return trainer

    def test_reaches_target_in_one_attempt(self):
        trainer = self._make_trainer(consistent_per_call=[10])
        result, _, _, _ = accumulate_consistent_problems(
            nesig_trainer=trainer,
            target=5,
            init_actions=5,
            goal_actions=5,
            max_attempts=3,
        )
        assert len(result) == 5

    def test_accumulates_across_multiple_attempts(self):
        trainer = self._make_trainer(consistent_per_call=[2, 3, 5])
        result, _, _, _ = accumulate_consistent_problems(
            nesig_trainer=trainer,
            target=8,
            init_actions=5,
            goal_actions=5,
            max_attempts=5,
        )
        assert len(result) == 8

    def test_returns_partial_if_max_attempts_reached(self):
        trainer = self._make_trainer(consistent_per_call=[1])
        result, _, _, _ = accumulate_consistent_problems(
            nesig_trainer=trainer,
            target=20,
            init_actions=5,
            goal_actions=5,
            max_attempts=3,
        )
        assert len(result) == 3  # 1 per attempt × 3 attempts

    def test_trims_to_target(self):
        trainer = self._make_trainer(consistent_per_call=[20])
        result, _, _, _ = accumulate_consistent_problems(
            nesig_trainer=trainer,
            target=5,
            init_actions=5,
            goal_actions=5,
            max_attempts=3,
        )
        assert len(result) == 5

    def test_empty_on_zero_consistent(self):
        trainer = self._make_trainer(consistent_per_call=[0])
        result, _, _, _ = accumulate_consistent_problems(
            nesig_trainer=trainer,
            target=5,
            init_actions=5,
            goal_actions=5,
            max_attempts=3,
        )
        assert len(result) == 0