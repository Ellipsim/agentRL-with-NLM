"""
> test_debug_actions.py

Debug test to understand why action_name_to_ind doesn't have certain actions.
This test investigates the mismatch between:
  - Actions available at initial state (what NLM learns)
  - Actions available in actual problems (what tests expect)
"""

import pytest
import torch
import argparse
from pathlib import Path
from lifted_pddl import Parser

from src.agent.pddl.pddl_problem import PDDLProblem
from src.agent.learning.model_wrapper import NLMWrapperActor


@pytest.fixture
def mock_args():
    """Create mock arguments for NLMWrapperActor."""
    return argparse.Namespace(
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
def device():
    """Get device (CPU for testing)."""
    return torch.device("cpu")


class TestDebugActions:
    """Debug tests to understand action_name_to_ind issue"""

    def test_domain_actions(self, parser):
        """Test 1: What actions are defined in the domain?"""
        print("\n" + "="*70)
        print("TEST 1: DOMAIN ACTIONS")
        print("="*70)
        
        domain_actions = set()
        for action in parser.actions:
            action_name = action[0]
            domain_actions.add(action_name)
            print(f"  ✓ {action_name}")
        
        print(f"\nTotal domain actions: {len(domain_actions)}")
        print(f"Domain actions: {sorted(domain_actions)}")
        
        # Assert we have the expected blocksworld actions
        expected = {'pick-up', 'put-down', 'stack', 'unstack'}
        assert domain_actions == expected, f"Expected {expected}, got {domain_actions}"

    def test_initial_state_applicable_actions(self, parser, problem_file):
        """Test 2: What actions are applicable in INITIAL state?"""
        print("\n" + "="*70)
        print("TEST 2: INITIAL STATE APPLICABLE ACTIONS")
        print("="*70)
        
        # Load problem
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=50)
        initial_state = problem.initial_state
        
        print(f"Problem file: {problem_file}")
        print(f"Objects: {initial_state.objects}")
        print(f"Atoms in initial state: {initial_state.atoms}")
        
        # Get applicable actions at initial state
        applicable_ground = problem.applicable_ground_actions()
        applicable_lifted = problem.applicable_lifted_actions()
        
        print(f"\nApplicable ground actions: {len(applicable_ground)}")
        for action in sorted(applicable_ground)[:5]:  # Show first 5
            print(f"  - {action}")
        
        print(f"\nApplicable lifted actions (unique names): {len(applicable_lifted)}")
        for action_name in sorted(applicable_lifted):
            print(f"  - {action_name}")
        
        assert len(applicable_lifted) > 0, "Should have at least one applicable action"

    def test_nlm_wrapper_initialization(self, mock_args, parser, problem_file, device):
        """Test 3: What actions does NLMWrapperActor see?"""
        print("\n" + "="*70)
        print("TEST 3: NLM WRAPPER INITIALIZATION")
        print("="*70)
        
        # Create dummy state from problem
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=50)
        dummy_state = problem.initial_state
        
        print(f"Initializing NLM with state from: {problem_file}")
        
        # Initialize NLM
        actor_args = {"dummy_pddl_state": dummy_state}
        actor = NLMWrapperActor(mock_args, actor_args, device)
        
        # Check what's in action_name_to_ind
        print(f"\naction_name_to_ind dictionary:")
        print(f"  Keys: {list(actor.action_name_to_ind.keys())}")
        print(f"  Values: {list(actor.action_name_to_ind.values())}")
        
        nlm_actions = set(actor.action_name_to_ind.keys())
        print(f"\nNLM knows about {len(nlm_actions)} actions: {sorted(nlm_actions)}")
        
        assert len(nlm_actions) > 0, "NLM should know about at least one action"

    def test_action_mismatch_across_problems(self, mock_args, fresh_parser, parser, problem_file, device):
        """Test 4: Do different problems have different applicable actions?"""
        print("\n" + "="*70)
        print("TEST 4: ACTION MISMATCH ACROSS PROBLEMS")
        print("="*70)
        
        # Initialize NLM with dummy_pddl_state (using parser fixture)
        problem1 = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=50)
        dummy_state = problem1.initial_state
        
        actor_args = {"dummy_pddl_state": dummy_state}
        actor = NLMWrapperActor(mock_args, actor_args, device)
        nlm_actions = set(actor.action_name_to_ind.keys())
        
        print(f"NLM initialized with: {problem_file}")
        print(f"NLM knows about: {sorted(nlm_actions)}")
        
        # Load problem with fresh_parser (as test does)
        problem2 = PDDLProblem.load_from_pddl(fresh_parser(), problem_file, max_actions=50)
        applicable = problem2.applicable_ground_actions()
        problem_actions = set(action[0] for action in applicable)
        
        print(f"\nProblem loaded with fresh_parser: {problem_file}")
        print(f"Problem has applicable actions: {sorted(problem_actions)}")
        
        # Compare
        print(f"\nComparison:")
        print(f"  NLM actions: {sorted(nlm_actions)}")
        print(f"  Problem actions: {sorted(problem_actions)}")
        print(f"  Intersection: {sorted(nlm_actions & problem_actions)}")
        print(f"  Missing in NLM: {sorted(problem_actions - nlm_actions)}")
        print(f"  Extra in NLM: {sorted(nlm_actions - problem_actions)}")
        
        # This is the critical assertion - they should match!
        if nlm_actions != problem_actions:
            print(f"\n⚠️  MISMATCH DETECTED!")
            print(f"   This is why forward() fails with KeyError")

    def test_check_all_problems_have_same_actions(self, mock_args, fresh_parser, parser, device):
        """Test 5: Do all problem files have the same applicable actions?"""
        print("\n" + "="*70)
        print("TEST 5: CONSISTENCY ACROSS ALL PROBLEMS")
        print("="*70)
        
        problem_files = sorted(Path('data/problems').glob('*.pddl'))
        print(f"Found {len(problem_files)} problem files\n")
        
        all_actions_by_problem = {}
        
        for problem_file in problem_files:
            try:
                problem = PDDLProblem.load_from_pddl(fresh_parser(), problem_file, max_actions=50)
                applicable = problem.applicable_ground_actions()
                action_names = set(action[0] for action in applicable)
                all_actions_by_problem[problem_file.name] = action_names
                
                print(f"  {problem_file.name}: {sorted(action_names)}")
            except Exception as e:
                print(f"  {problem_file.name}: ERROR - {e}")
        
        # Check if all problems have same actions
        print(f"\nChecking consistency:")
        action_sets = list(all_actions_by_problem.values())
        
        if action_sets:
            first_set = action_sets[0]
            all_same = all(s == first_set for s in action_sets)
            
            if all_same:
                print(f"  ✓ All problems have the same applicable actions")
            else:
                print(f"  ✗ PROBLEMS HAVE DIFFERENT APPLICABLE ACTIONS!")
                for name, actions in all_actions_by_problem.items():
                    if actions != first_set:
                        print(f"    {name} differs: {actions - first_set} missing, {first_set - actions} extra")

    def test_initial_state_vs_domain_actions(self, parser, problem_file):
        """Test 6: Why might initial state not have all domain actions?"""
        print("\n" + "="*70)
        print("TEST 6: INITIAL STATE vs DOMAIN ACTIONS")
        print("="*70)
        
        # Domain actions
        domain_actions = {action[0] for action in parser.actions}
        print(f"Domain actions: {sorted(domain_actions)}")
        
        # Initial state actions
        problem = PDDLProblem.load_from_pddl(parser, problem_file, max_actions=50)
        initial_applicable = problem.applicable_lifted_actions()
        
        print(f"Initial state applicable: {sorted(initial_applicable)}")
        
        # Difference
        missing = domain_actions - set(initial_applicable)
        if missing:
            print(f"\n⚠️  Actions NOT applicable in initial state: {missing}")
            print("\nThis is the ROOT CAUSE of the issue!")
            print("NLM is initialized with only applicable actions at initial state,")
            print("but test problems may have different applicable actions.")