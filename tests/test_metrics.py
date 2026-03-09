"""
> test_problem_solver_metrics_real.py

Tests for ProblemSolver using real PDDL problem files from conftest fixtures.

Uses fixtures from conftest.py:
  - parser: Parser loaded with blocksworld domain
  - problem_file: Automatically parametrized for each .pddl file in data/problems/

Tests automatically run for each problem file in data/problems/
"""

import pytest
from pathlib import Path
from unittest.mock import Mock

from src.agent.pddl.problem_solver import ProblemSolver
from src.agent.pddl.pddl_problem import PDDLProblem
from src.agent.learning.generative_policy import GenerativePolicy


@pytest.fixture
def mock_policy():
    """Create a mock policy that selects first available action"""
    policy = Mock(spec=GenerativePolicy)
    
    def mock_select_actions(problems, applicable_actions_list):
        # Select first action from each problem's applicable actions
        chosen_actions = [actions[0] if actions else Mock() 
                         for actions in applicable_actions_list]
        action_log_probs = [-1.0 for _ in chosen_actions]
        internal_states = [Mock() for _ in chosen_actions]
        return chosen_actions, action_log_probs, internal_states
    
    policy.select_actions.side_effect = mock_select_actions
    return policy


class TestProblemSolverBasics:
    """Basic tests that don't require parametrization"""
    
    def test_solver_initialization(self, parser):
        """Test ProblemSolver initializes correctly with parser"""
        policy = Mock(spec=GenerativePolicy)
        
        solver = ProblemSolver(
            parser,
            policy,
            reward_goal_reached=1.0,
            reward_step=-0.01,
            reward_efficiency=0.5
        )
        
        assert solver.parser is parser
        assert solver.policy is policy
        assert solver.reward_goal_reached == 1.0
        assert solver.reward_step == -0.01
        assert solver.reward_efficiency == 0.5
    
    def test_solver_default_rewards(self, parser):
        """Test ProblemSolver uses default reward weights"""
        policy = Mock(spec=GenerativePolicy)
        solver = ProblemSolver(parser, policy)
        
        assert solver.reward_goal_reached == 1.0
        assert solver.reward_step == -0.01
        assert solver.reward_efficiency == 0.5


class TestProblemSolverWithSingleProblem:
    """Tests that load and solve a single problem file"""
    
    def test_load_problem_from_file(self, parser, problem_file):
        """Test loading a problem from file"""
        problem = PDDLProblem.load_from_pddl(parser, str(problem_file))
        
        assert problem is not None
        assert problem.initial_state is not None
        assert problem.goal is not None
    
    def test_solve_problem_with_budget(self, parser, problem_file, mock_policy):
        """Test solving a problem with action budget"""
        solver = ProblemSolver(parser, mock_policy)
        problem = PDDLProblem.load_from_pddl(parser, str(problem_file))
        
        is_solved, problem_info, trajectories, elapsed = solver.solve_problems(
            [problem],
            list_max_actions=50
        )
        
        # Verify structure
        assert len(is_solved) == 1
        assert len(problem_info) == 1
        assert len(trajectories) == 1
        assert elapsed >= 0
        
        # Verify problem info
        info = problem_info[0]
        assert 'goal_reached' in info
        assert 'num_steps' in info
        assert 'efficiency' in info
        assert 'success' in info
        assert 'solution_ratio' in info
        assert 'num_objects' in info
        assert 'num_goal_atoms' in info
    
    def test_metrics_structure(self, parser, problem_file, mock_policy):
        """Test that metrics are correctly structured"""
        solver = ProblemSolver(parser, mock_policy)
        problem = PDDLProblem.load_from_pddl(parser, str(problem_file))
        
        is_solved, problem_info, trajectories, elapsed = solver.solve_problems(
            [problem],
            list_max_actions=50
        )
        
        info = problem_info[0]
        
        # Efficiency should be in [0, 1]
        assert 0 <= info['efficiency'] <= 1
        
        # Solution ratio should be in [0, 1]
        assert 0 <= info['solution_ratio'] <= 1
        
        # num_steps should be non-negative
        assert info['num_steps'] >= 0
        
        # success should equal goal_reached
        assert info['success'] == info['goal_reached']
        
        # num_objects should be a dict
        assert isinstance(info['num_objects'], dict)
        
        # num_goal_atoms should be non-negative
        assert info['num_goal_atoms'] >= 0
    
    def test_trajectory_rewards_populated(self, parser, problem_file, mock_policy):
        """Test that trajectory samples have rewards populated"""
        solver = ProblemSolver(parser, mock_policy)
        problem = PDDLProblem.load_from_pddl(parser, str(problem_file))
        
        is_solved, problem_info, trajectories, elapsed = solver.solve_problems(
            [problem],
            list_max_actions=50
        )
        
        trajectory = trajectories[0]
        
        # Check that all samples have reward field
        for sample in trajectory:
            assert 'reward' in sample
            assert isinstance(sample['reward'], (int, float))
            
            # All other required fields should be present
            assert 'state' in sample
            assert 'internal_state' in sample
            assert 'applicable_actions' in sample
            assert 'chosen_action' in sample
            assert 'chosen_action_ind' in sample
            assert 'action_log_prob' in sample
    
    def test_reward_shaping_on_real_problem(self, parser, problem_file, mock_policy):
        """Test reward shaping logic on real problem"""
        solver = ProblemSolver(
            parser,
            mock_policy,
            reward_goal_reached=1.0,
            reward_step=-0.01,
            reward_efficiency=0.5
        )
        problem = PDDLProblem.load_from_pddl(parser, str(problem_file))
        
        is_solved, problem_info, trajectories, elapsed = solver.solve_problems(
            [problem],
            list_max_actions=100
        )
        
        trajectory = trajectories[0]
        info = problem_info[0]
        
        if len(trajectory) > 0:
            # First step should have negative or zero reward (cost)
            assert trajectory[0]['reward'] <= 0, "First step should be penalized"
            
            # If goal reached, last step should have goal bonus + efficiency
            if info['goal_reached']:
                last_reward = trajectory[-1]['reward']
                # Should be: -0.01 + 1.0 + efficiency_bonus
                assert last_reward > 0, "Last step of solved problem should be positive"
                assert last_reward >= 0.9, "Should have significant goal bonus"
            else:
                # If not solved, all steps should be negative (cost only)
                for sample in trajectory:
                    assert sample['reward'] <= 0, "Failed problem should have all negative rewards"
    
    def test_efficiency_metric_logic(self, parser, problem_file, mock_policy):
        """Test efficiency metric calculation"""
        solver = ProblemSolver(parser, mock_policy)
        problem = PDDLProblem.load_from_pddl(parser, str(problem_file))
        
        is_solved, problem_info, trajectories, elapsed = solver.solve_problems(
            [problem],
            list_max_actions=50
        )
        
        info = problem_info[0]
        
        # If goal reached: efficiency = 1 - (steps / max_steps)
        if info['goal_reached']:
            expected_efficiency = 1.0 - (info['num_steps'] / 50)
            assert abs(info['efficiency'] - expected_efficiency) < 0.001
            
        # If not reached: efficiency = 0
        else:
            assert info['efficiency'] == 0.0
    
    def test_different_budgets_same_problem(self, fresh_parser, problem_file, mock_policy):
        """Test same problem with different action budgets"""
        solver = ProblemSolver(fresh_parser(), mock_policy)
        
        budgets = [5, 10, 20, 50]
        results = []
        
        for budget in budgets:
            problem = PDDLProblem.load_from_pddl(fresh_parser(), str(problem_file))
            is_solved, info, traj, elapsed = solver.solve_problems([problem], budget)
            
            results.append({
                'budget': budget,
                'solved': info[0]['goal_reached'],
                'steps': info[0]['num_steps'],
                'efficiency': info[0]['efficiency']
            })
        
        # Verify results make sense
        assert len(results) == 4
        for r in results:
            assert 0 <= r['efficiency'] <= 1
            assert r['steps'] >= 0


class TestProblemSolverCustomRewards:
    """Test custom reward configurations"""
    
    def test_custom_reward_weights(self, parser, problem_file, mock_policy):
        """Test that custom reward weights are applied"""
        problem = PDDLProblem.load_from_pddl(parser, str(problem_file))
        
        # Test with increased goal reward
        solver_high = ProblemSolver(
            parser,
            mock_policy,
            reward_goal_reached=2.0,  # Doubled
            reward_step=-0.01,
            reward_efficiency=0.5
        )
        
        is_solved, info, traj, _ = solver_high.solve_problems([problem], 50)
        
        if info[0]['goal_reached'] and len(traj[0]) > 0:
            high_reward = traj[0][-1]['reward']
            
            # Reset problem for second test
            problem.reset()
            
            # Test with standard goal reward
            solver_normal = ProblemSolver(
                parser,
                mock_policy,
                reward_goal_reached=1.0,
                reward_step=-0.01,
                reward_efficiency=0.5
            )
            
            is_solved2, info2, traj2, _ = solver_normal.solve_problems([problem], 50)
            normal_reward = traj2[0][-1]['reward']
            
            # High reward version should have higher reward
            # Difference should be approximately 1.0 (the extra goal bonus)
            assert high_reward > normal_reward
            assert abs((high_reward - normal_reward) - 1.0) < 0.01


class TestProblemSolverEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_zero_budget(self, parser, problem_file, mock_policy):
        """Test with zero action budget"""
        solver = ProblemSolver(parser, mock_policy)
        problem = PDDLProblem.load_from_pddl(parser, str(problem_file))
        
        is_solved, info, traj, _ = solver.solve_problems([problem], 0)
        
        # With zero budget, should not solve
        assert info[0]['goal_reached'] is False
        assert info[0]['efficiency'] == 0.0
    
    def test_very_large_budget(self, parser, problem_file, mock_policy):
        """Test with very large action budget"""
        solver = ProblemSolver(parser, mock_policy)
        problem = PDDLProblem.load_from_pddl(parser, str(problem_file))
        
        is_solved, info, traj, _ = solver.solve_problems([problem], 10000)
        
        # Should complete without error
        assert len(info) == 1
        assert isinstance(info[0]['efficiency'], float)
    
    def test_problem_independence(self, fresh_parser, problem_file, mock_policy):
        """Test that solving a problem doesn't affect subsequent solves"""
        solver = ProblemSolver(fresh_parser(), mock_policy)
        
        problem1 = PDDLProblem.load_from_pddl(fresh_parser(), str(problem_file))
        problem2 = PDDLProblem.load_from_pddl(fresh_parser(), str(problem_file))
        
        # Solve first
        is_solved1, info1, traj1, _ = solver.solve_problems([problem1], 50)
        
        # Problem should be reset
        problem1.reset()
        
        # Solve again
        is_solved2, info2, traj2, _ = solver.solve_problems([problem1], 50)
        
        # Results should be identical
        assert info1[0]['goal_reached'] == info2[0]['goal_reached']
        assert info1[0]['num_steps'] == info2[0]['num_steps']


class TestProblemSolverBatch:
    """Test batch solving with real problems"""
    
    def test_batch_solve_multiple_problems(self, fresh_parser, problem_file, mock_policy):
        """Test solving multiple problems in a batch"""
        solver = ProblemSolver(fresh_parser(), mock_policy)
        
        # Load same problem multiple times
        problems = [
            PDDLProblem.load_from_pddl(fresh_parser(), str(problem_file))
            for _ in range(3)
        ]
        
        is_solved, problem_info, trajectories, elapsed = solver.solve_problems(
            problems,
            list_max_actions=50
        )
        
        # Verify batch results
        assert len(is_solved) == 3
        assert len(problem_info) == 3
        assert len(trajectories) == 3
        
        # All should have complete metrics
        for info in problem_info:
            assert 'goal_reached' in info
            assert 'efficiency' in info
            assert 'success' in info
    
    def test_batch_with_different_budgets(self, fresh_parser, problem_file, mock_policy):
        """Test batch solving with different budgets per problem"""
        solver = ProblemSolver(fresh_parser(), mock_policy)
        
        problems = [
            PDDLProblem.load_from_pddl(fresh_parser(), str(problem_file))
            for _ in range(3)
        ]
        
        budgets = [10, 50, 100]
        
        is_solved, problem_info, trajectories, elapsed = solver.solve_problems(
            problems,
            list_max_actions=budgets
        )
        
        # Verify each problem got correct budget
        for i, info in enumerate(problem_info):
            assert info['max_actions'] == budgets[i]


# ============================================================================
# Usage Instructions
# ============================================================================

"""
To run these tests:

1. Make sure your conftest.py is in the tests/ directory
2. Make sure your problems are in data/problems/
3. Make sure your domain is at data/domains/blocksworld.pddl

Then run:

    pytest test_problem_solver_metrics_real.py -v
    
To run with output:

    pytest test_problem_solver_metrics_real.py -v -s
    
To run specific test class:

    pytest test_problem_solver_metrics_real.py::TestProblemSolverBasics -v
    
To run specific test:

    pytest test_problem_solver_metrics_real.py::TestProblemSolverWithSingleProblem::test_load_problem_from_file -v

To see which problems are being tested:

    pytest test_problem_solver_metrics_real.py --collect-only

The pytest_generate_tests in conftest.py automatically parametrizes tests 
that use the problem_file fixture, so each test runs for every .pddl file 
in data/problems/
"""