"""
> evaluate_per_level.py

Offline evaluation script. Discovers all per-level-advance checkpoints saved
during training, evaluates each policy snapshot across all difficulty levels,
and produces:
  - One JSON + plot per checkpoint  (eval_advance_level{L}_step{S}.*)
  - One combined success-rate plot  (all_advance_evals.png)

Usage:
    python -m src.scripts.evaluate_policy_per_level \
        --experiment-id <id> \
        --domain-path data/domains/blocksworld.pddl
"""

import argparse
import os
import re
import torch
import json
from pathlib import Path
from os.path import dirname, abspath
from pytorch_lightning import seed_everything
from lifted_pddl import Parser
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
import random
import subprocess

from src.agent.constants import CKPTS_FOLDER_NAME, EXPERIMENT_INFO_FILENAME
from src.agent.learning.generative_policy import PPOSolverPolicy
from src.agent.learning.model_wrapper import NLMWrapperActor, NLMWrapperCritic
from src.agent.pddl.problem_solver import ProblemSolver
from src.agent.pddl.pddl_state import PDDLState
from src.agent.pddl.pddl_problem import PDDLProblem


# =====================================================================
# Curriculum Utilities (inlined to avoid circular imports)
# =====================================================================

def get_level_blocks(args, level: int):
    min_blocks = args.min_blocks_start + (level - 1) * args.blocks_increment
    max_blocks = args.max_blocks_start + (level - 1) * args.blocks_increment
    return min_blocks, max_blocks


def generate_problems(generator_path: str, out_dir: str,
                      count: int, min_blocks: int, max_blocks: int,
                      seed_start: int = 0) -> None:
    import subprocess
    out_path = Path(out_dir)
    out_path.mkdir(parents=True, exist_ok=True)
    for f in out_path.glob("*.pddl"):
        f.unlink()
    print(f"    Generating {count} problems ({min_blocks}-{max_blocks} blocks) -> {out_dir}")
    for i in range(count):
        blocks = random.randint(min_blocks, max_blocks)
        seed = seed_start + i
        out_file = out_path / f"problem_{i + 1}.pddl"
        result = subprocess.run(
            [generator_path, '4', str(blocks), str(seed)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"Generator failed for problem {i + 1}: {result.stderr}")
        out_file.write_text(result.stdout)


def load_problems_from_dir(
    problem_dir,
    domain_path,
    num_problems,
    max_actions=None,
) -> list:
    problem_dir = Path(problem_dir)
    problem_files = sorted(problem_dir.glob("*.pddl"))
    if not problem_files:
        raise FileNotFoundError(f"No .pddl files in {problem_dir}")
    problems = []
    for i in range(num_problems):
        path = str(problem_files[i % len(problem_files)])
        fresh_parser = Parser()
        fresh_parser.parse_domain(str(domain_path))
        problem = PDDLProblem.load_from_pddl(fresh_parser, path)
        if problem is not None:
            if max_actions is not None:
                problem.max_actions = (
                    max_actions[i % len(max_actions)]
                    if isinstance(max_actions, tuple)
                    else max_actions
                )
            problems.append(problem)
    return problems


# =====================================================================
# Argument Parsing
# =====================================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Offline evaluation of all level-advance checkpoints.",
    )
    parser.add_argument('--experiment-id', type=str, required=True)
    parser.add_argument('--experiments-dir', type=str, default='./experiments')
    parser.add_argument('--domain-path', type=str, required=True)
    parser.add_argument('--generator-path', type=str,
                        default='./problem_generator/pddl-generators/blocksworld/blocksworld')
    parser.add_argument('--data-dir', type=str, default='./data/problems/eval')
    parser.add_argument('--num-problems-per-level', type=int, default=50)
    parser.add_argument('--device', type=str, choices=('gpu', 'cpu'), default='gpu')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--seed-start', type=int, default=888000)
    parser.add_argument('--force-reeval', action='store_true',
                        help="Re-evaluate even if results JSON already exists")
    return parser.parse_args()


# =====================================================================
# Checkpoint Discovery
# =====================================================================

def discover_level_checkpoints(experiment_folder_path: Path) -> List[Tuple[int, int, Path]]:
    ckpt_dir = experiment_folder_path / CKPTS_FOLDER_NAME / 'level_advances'
    pattern = re.compile(r'level(\d+)_step(\d+)\.ckpt')
    checkpoints = []

    if ckpt_dir.exists():
        for f in ckpt_dir.glob('level*_step*.ckpt'):
            match = pattern.match(f.name)
            if match:
                level = int(match.group(1))
                step = int(match.group(2))
                checkpoints.append((level, step, f))

    checkpoints = sorted(checkpoints, key=lambda x: x[1])

    # Always append the final checkpoint if it exists
    last_ckpt = experiment_folder_path / CKPTS_FOLDER_NAME / 'last.ckpt'
    if last_ckpt.exists():
        last_level = checkpoints[-1][0] if checkpoints else 0
        last_step = checkpoints[-1][1] if checkpoints else 0
        # Only add if it's not already covered by a level-advance checkpoint
        if not checkpoints or last_ckpt != checkpoints[-1][2]:
            checkpoints.append((-1, last_step, last_ckpt))  # -1 signals "final"

    return checkpoints


# =====================================================================
# Policy Loading
# =====================================================================

def load_policy_from_checkpoint(ckpt_path: Path, info: Dict,
                                 domain_parser, device: torch.device) -> PPOSolverPolicy:
    """Build and load a policy from a checkpoint file."""
    domain_actions = set([
        (action[0], tuple([var for var, var_class in zip(action[1][0], action[1][1])
                           if var_class == 'param']))
        for action in domain_parser.actions
    ])
    dummy_state = PDDLState(
        types=domain_parser.types,
        type_hierarchy=domain_parser.type_hierarchy,
        predicates=domain_actions,
        objects=[],
        atoms=set()
    )
    policy = PPOSolverPolicy(
        args=info,
        actor_class=NLMWrapperActor,
        actor_arguments={'dummy_pddl_state': dummy_state},
        critic_class=NLMWrapperCritic,
        critic_arguments={'dummy_pddl_state': dummy_state},
        device=device,
    )
    checkpoint = torch.load(str(ckpt_path), map_location=device)
    policy.load_state_dict(checkpoint['state_dict'])
    policy.eval()
    if device.type == 'cuda':
        policy.to('cuda')
    return policy


# =====================================================================
# Evaluation
# =====================================================================

def evaluate_per_level(
    info: Dict,
    domain_parser,
    policy,
    problem_solver: ProblemSolver,
    generator_path: str,
    domain_path: str,
    data_dir: str,
    num_problems_per_level: int,
    seed_start: int,
) -> Dict[int, Dict]:
    """Evaluate a policy snapshot across all curriculum levels."""

    results = {}
    max_levels = info['max_levels']
    max_actions_test = info['max_actions_test']

    class FakeArgs:
        pass
    fake_args = FakeArgs()
    fake_args.min_blocks_start = info['min_blocks_start']
    fake_args.max_blocks_start = info['max_blocks_start']
    fake_args.blocks_increment = info['blocks_increment']
    fake_args.max_levels = max_levels

    for level in range(1, max_levels + 1):
        min_blocks, max_blocks = get_level_blocks(fake_args, level)
        eval_dir = Path(data_dir) / f'level_{level}'

        print(f"    Level {level}/{max_levels} ({min_blocks}-{max_blocks} blocks)...")

        generate_problems(
            generator_path, str(eval_dir),
            num_problems_per_level,
            min_blocks, max_blocks,
            seed_start=seed_start + level * 100,
        )
        problems = load_problems_from_dir(
            str(eval_dir), domain_path,
            num_problems_per_level,
            max_actions=max_actions_test,
        )

        with torch.no_grad():
            _, problem_info, _, _ = problem_solver.solve_problems(
                problems, list_max_actions=max_actions_test
            )

        success_count = sum(1 for p in problem_info if p['goal_reached'])
        success_rate = success_count / len(problem_info) if problem_info else 0.0
        successful = [p for p in problem_info if p['goal_reached']]
        mean_efficiency = (sum(p['efficiency'] for p in successful) / len(successful)
                           if successful else 0.0)
        mean_steps = (sum(p['num_steps'] for p in successful) / len(successful)
                      if successful else 0.0)

        results[level] = {
            'min_blocks': min_blocks,
            'max_blocks': max_blocks,
            'success_rate': success_rate,
            'mean_efficiency': mean_efficiency,
            'mean_steps': mean_steps,
            'num_successful': success_count,
            'num_problems': len(problem_info),
        }
        print(f"      success={success_rate:.1%}  efficiency={mean_efficiency:.3f}  steps={mean_steps:.1f}")

    return results


# =====================================================================
# Plotting
# =====================================================================

def plot_single_eval(results: Dict, title: str, save_path: str):
    levels = sorted(results.keys(), key=int)
    labels = [f"L{l}\n({results[l]['min_blocks']}-{results[l]['max_blocks']})" for l in levels]
    success_rates = [results[l]['success_rate'] * 100 for l in levels]
    efficiencies = [results[l]['mean_efficiency'] for l in levels]
    mean_steps = [results[l]['mean_steps'] for l in levels]

    num_levels = len(levels)
    fig, axes = plt.subplots(1, 3, figsize=(max(15, num_levels * 1.2), 6))  # wider
    fig.suptitle(title, fontsize=13)

    for ax, values, color, ylabel, ylim, fmt in [
        (axes[0], success_rates, 'steelblue', 'Success Rate (%)', (0, 110), '{:.1f}%'),
        (axes[1], efficiencies,  'seagreen',  'Efficiency',        (0, 1.1), '{:.3f}'),
        (axes[2], mean_steps,    'coral',     'Steps',             (None, None), '{:.1f}'),
    ]:
        ax.bar(range(num_levels), values, color=color)
        ax.set_xticks(range(num_levels))
        ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=8)  # rotated
        ax.set_title(ylabel)
        ax.set_xlabel('Level (blocks)')
        if ylim[0] is not None:
            ax.set_ylim(*ylim)
        for i, v in enumerate(values):
            offset = 1 if color == 'steelblue' else (0.01 if color == 'seagreen' else 0.1)
            ax.text(i, v + offset, fmt.format(v), ha='center', fontsize=8)

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"    Saved plot: {save_path}")


def plot_all_success_rates(
    all_results: List[Tuple[int, int, Dict]],
    save_path: str,
):
    num_evals = len(all_results)
    fig, axes = plt.subplots(1, num_evals, figsize=(5 * num_evals, 6), sharey=True)
    fig.suptitle('Success Rate per Level — All Curriculum Advances', fontsize=14)

    if num_evals == 1:
        axes = [axes]

    for ax, (level, step, results) in zip(axes, all_results):
        levels = sorted(results.keys(), key=int)
        labels = [f"L{l}\n({results[l]['min_blocks']}-{results[l]['max_blocks']})"
                  for l in levels]
        success_rates = [results[l]['success_rate'] * 100 for l in levels]

        num_levels = len(levels)
        bars = ax.bar(range(num_levels), success_rates, color='steelblue')

        ax.set_xticks(range(num_levels))
        ax.set_xticklabels(labels, rotation=45, ha='right', fontsize=8)  # rotated

        # Fix title: use "Final" for level == -1
        title_str = 'Final checkpoint' if level == -1 else f'After level {level}'
        ax.set_title(f'{title_str}\n(step {step})', fontsize=10)

        ax.set_ylim(0, 115)  # extra headroom for annotations
        ax.set_xlabel('Level (blocks)')
        if ax is axes[0]:
            ax.set_ylabel('Success Rate (%)')

        for bar, v in zip(bars, success_rates):
            ax.text(bar.get_x() + bar.get_width() / 2, v + 1,
                    f'{v:.1f}%', ha='center', fontsize=7, rotation=45)  # rotated annotations too

    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\n  Saved combined plot: {save_path}")


# =====================================================================
# Entry Point
# =====================================================================

def main():
    os.chdir(dirname(dirname(dirname(abspath(__file__)))))
    args = parse_arguments()
    seed_everything(args.seed, workers=True)

    experiment_folder_path = Path(args.experiments_dir) / args.experiment_id
    device = torch.device('cuda' if args.device == 'gpu' else 'cpu')

    # Load experiment info
    experiment_info_path = experiment_folder_path / EXPERIMENT_INFO_FILENAME
    if not experiment_info_path.exists():
        raise FileNotFoundError(f"Experiment info not found: {experiment_info_path}")
    with open(experiment_info_path) as f:
        info = json.load(f)

    # Discover checkpoints
    checkpoints = discover_level_checkpoints(experiment_folder_path)
    if not checkpoints:
        print("No checkpoints found. Did you train with --save-level-checkpoints?")
        return

    print(f"\n>>> Found {len(checkpoints)} checkpoint(s)\n")

    domain_parser = Parser()
    domain_parser.parse_domain(args.domain_path)

    all_results: List[Tuple[int, int, Dict]] = []

    for level, step, ckpt_path in checkpoints:
        label = 'final' if level == -1 else f'level{level}'
        print(f"  Evaluating: {label}  step={step}  ckpt={ckpt_path.name}")

        results_path = experiment_folder_path / f'eval_advance_{label}_step{step}.json'

        # Skip if already evaluated and not forcing re-evaluation
        if results_path.exists() and not args.force_reeval:
            print(f"    Already evaluated, loading from {results_path.name}")
            with open(results_path) as f:
                results = json.load(f)
        else:
            policy = load_policy_from_checkpoint(ckpt_path, info, domain_parser, device)
            problem_solver = ProblemSolver(
                domain_parser, policy,
                reward_goal_reached=info['reward_goal_reached'],
                reward_step=info['reward_step'],
                reward_efficiency=info['reward_efficiency'],
            )
            results = evaluate_per_level(
                info=info,
                domain_parser=domain_parser,
                policy=policy,
                problem_solver=problem_solver,
                generator_path=args.generator_path,
                domain_path=args.domain_path,
                data_dir=str(Path(args.data_dir) / f'{label}_step{step}'),
                num_problems_per_level=args.num_problems_per_level,
                seed_start=args.seed_start,
            )
            # Save JSON
            with open(results_path, 'w') as f:
                json.dump(results, f, indent=2)

            # Save individual plot
            title = f'Policy Evaluation — {"Final checkpoint" if level == -1 else f"After level {level}"} (step {step})'
            plot_single_eval(
                results,
                title=title,
                save_path=str(experiment_folder_path / f'eval_advance_{label}_step{step}.png'),
            )

        all_results.append((level, step, results))

    # Combined success-rate plot
    plot_all_success_rates(
        all_results,
        save_path=str(experiment_folder_path / 'all_advance_evals.png'),
    )

    print(f"\n>>> Done!")


if __name__ == '__main__':
    main()