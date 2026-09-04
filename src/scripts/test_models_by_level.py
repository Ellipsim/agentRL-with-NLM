"""
> test_models_by_level.py

Evaluate every trained student checkpoint under an experiments directory on
blocksworld test problems of increasing difficulty (number of blocks), and
plot the mean success rate per difficulty level across all models.

It reuses the exact same machinery train_and_test_NeSIG.py uses:
  - create_policy / read_last_train_it   (load a trained checkpoint)
  - load_problems_from_dir               (load PDDLProblem objects)
  - generate_problems                    (call the blocksworld pddl-generator)
  - StudentTrainer._solve_and_collect_trajectories + .log_metrics
    (exact same code path your training script uses for its final test eval)


--------------------------------------------------------------------------
Usage:


python -m src.scripts.test_models_by_level --experiments-dir ./experiments/final_agent_nesig --domain-path data/domains/blocksworld.pddl --generator-path ./problem_generator/pddl-generators/blocksworld/blocksworld --min-blocks 3 --max-blocks 30 --num-problems-per-level 50 --test-problems-dir ./data/problems/test_by_level --output-plot ./results/success_by_level.png --output-csv ./results/success_by_level.csv --device cpu

"""

import argparse
import json
import shutil
import sys
import tempfile
import traceback
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import torch
import matplotlib.pyplot as plt
from lifted_pddl import Parser

from src.agent.constants import EXPERIMENT_INFO_FILENAME, CKPTS_FOLDER_NAME
from src.agent.controller.train_and_test_ACG import (
    generate_problems, create_policy, read_last_train_it,
)
from src.agent.controller.train_and_test_NeSIG import (
    load_problems_from_dir,
    parse_arguments as parse_nesig_training_arguments,
)
from src.agent.controller.trainer import PolicyTrainer as StudentTrainer
from src.agent.pddl.problem_solver import ProblemSolver


# =====================================================================
# Argument parsing
# =====================================================================

def parse_arguments():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Evaluate all trained student models across blocksworld "
                    "difficulty levels and plot mean success rate.",
    )

    parser.add_argument('--experiments-dir', type=str, default='./experiments',
                         help="Root folder containing one subfolder per trained experiment")
    parser.add_argument('--domain-path', type=str, required=True,
                         help="Shared domain PDDL file (must match what models were trained with)")
    parser.add_argument('--generator-path', type=str,
                         default='./problem_generator/pddl-generators/blocksworld/blocksworld',
                         help="Path to the blocksworld problem generator binary")

    parser.add_argument('--min-blocks', type=int, default=1)
    parser.add_argument('--max-blocks', type=int, default=30)
    parser.add_argument('--num-problems-per-level', type=int, default=20)

    parser.add_argument('--test-problems-dir', type=str, default='./data/problems/test_by_level',
                         help="Where per-level test problems are cached / generated")
    parser.add_argument('--regenerate-problems', action='store_true',
                         help="Force regeneration of test problems even if the cache exists")
    parser.add_argument('--seed-start', type=int, default=555111,
                         help="Base seed for problem generation (offset per level internally)")

    parser.add_argument('--max-actions-factor', type=float, default=4.0,
                         help="max_actions(level) = factor * (level - 1), floored at --max-actions-min")
    parser.add_argument('--max-actions-min', type=int, default=4,
                         help="Minimum action budget, used for very small levels")

    parser.add_argument('--device', type=str, choices=('gpu', 'cpu'), default='gpu')

    parser.add_argument('--output-plot', type=str, default='./results/success_by_level.png')
    parser.add_argument('--output-csv', type=str, default='./results/success_by_level.csv')
    parser.add_argument('--include-experiment-ids', type=str, nargs='*', default=None,
                         help="If given, only evaluate these experiment ids (folder names)")
    parser.add_argument('--skip-incomplete', action='store_true', default=True,
                         help="Skip experiment folders with no completed training iteration")

    return parser.parse_args()


# =====================================================================
# Experiment discovery + model loading
# =====================================================================

def discover_experiments(experiments_dir: Path, include_ids: Optional[List[str]]) -> List[Path]:
    """Return experiment folders that look like they have a trained checkpoint."""
    if not experiments_dir.exists():
        raise FileNotFoundError(f"Experiments dir not found: {experiments_dir}")

    candidates = sorted(p for p in experiments_dir.iterdir() if p.is_dir())
    if include_ids is not None:
        wanted = set(include_ids)
        candidates = [p for p in candidates if p.name in wanted]

    valid = []
    for exp_dir in candidates:
        info_path = exp_dir / EXPERIMENT_INFO_FILENAME
        ckpt_dir = exp_dir / CKPTS_FOLDER_NAME
        if info_path.exists() and ckpt_dir.exists():
            valid.append(exp_dir)
        else:
            print(f"  Skipping {exp_dir.name}: missing {EXPERIMENT_INFO_FILENAME} or "
                  f"{CKPTS_FOLDER_NAME}/")
    return valid


def build_default_train_args(domain_path: str) -> argparse.Namespace:
    """
    Get a fully-populated Namespace of DEFAULT training args by invoking
    train_and_test_NeSIG.py's own parser. This guarantees every attribute
    create_policy / the NLM wrapper / StudentTrainer might touch exists,
    even ones that experiment_info.json doesn't happen to save (e.g. the
    CLI-only --train-mode flag).
    """
    old_argv = sys.argv
    try:
        # Only --domain-path is required by that parser; everything else
        # falls back to its own defaults.
        sys.argv = ['train_and_test_NeSIG.py', '--domain-path', domain_path]
        defaults = parse_nesig_training_arguments()
    finally:
        sys.argv = old_argv
    return defaults


def load_experiment_args(experiment_folder_path: Path, domain_path: str) -> argparse.Namespace:
    """
    Reconstruct the argparse.Namespace originally used to train this experiment.

    Strategy: start from train_and_test_NeSIG.py's own argparse defaults (so
    every attribute the training code expects is present), then overlay
    whatever was actually saved to experiment_info.json for this run, then
    force a couple of eval-only overrides (train_mode='resume' so
    create_policy loads the checkpoint instead of reinitializing).

    ADJUST HERE if your experiment_info.json schema differs from what's
    assumed below (flat dict of args, or a dict with an "args" sub-key).
    """
    info_path = experiment_folder_path / EXPERIMENT_INFO_FILENAME
    with open(info_path) as f:
        info = json.load(f)

    if isinstance(info, dict) and 'args' in info and isinstance(info['args'], dict):
        saved_args_dict = info['args']
    elif isinstance(info, dict):
        saved_args_dict = info
    else:
        raise ValueError(
            f"Unrecognized experiment_info.json schema in {info_path}. "
            f"Top-level keys: {list(info.keys()) if isinstance(info, dict) else type(info)}"
        )

    merged = vars(build_default_train_args(domain_path))
    merged.update(saved_args_dict)   # values actually used for this run win
    merged['domain_path'] = domain_path
    merged['train_mode'] = 'resume'  # eval-only: never wipe/reinit, just load the checkpoint

    return argparse.Namespace(**merged)


def load_student_model(
    experiment_folder_path: Path,
    domain_path: str,
    device: torch.device,
) -> Optional[Tuple[argparse.Namespace, torch.nn.Module, ProblemSolver, int]]:
    """Load the final trained student checkpoint for one experiment. Returns
    None if the experiment has no completed training iterations."""

    train_args = load_experiment_args(experiment_folder_path, domain_path)

    last_it = read_last_train_it(experiment_folder_path / EXPERIMENT_INFO_FILENAME)
    if last_it == 0:
        print(f"  {experiment_folder_path.name}: no completed training iterations, skipping")
        return None

    domain_parser = Parser()
    domain_parser.parse_domain(domain_path)

    student_policy = create_policy(
        train_args, domain_parser, last_it, experiment_folder_path, device
    )
    if device.type == 'cuda':
        student_policy.to('cuda')
    student_policy.eval()

    student_solver = ProblemSolver(
        domain_parser, student_policy,
        reward_goal_reached=train_args.reward_goal_reached,
        reward_step=train_args.reward_step,
    )

    return train_args, student_policy, student_solver, last_it


# =====================================================================
# Test problems per level
# =====================================================================

def get_level_problems(
    level: int,
    args: argparse.Namespace,
    max_actions: int,
) -> list:
    """Generate (if needed) and load the test problems for one difficulty level."""
    level_dir = Path(args.test_problems_dir) / f'level_{level:02d}'

    needs_generation = args.regenerate_problems or not list(level_dir.glob('*.pddl'))
    if needs_generation:
        level_dir.mkdir(parents=True, exist_ok=True)
        print(f"    Generating {args.num_problems_per_level} problems for level={level} blocks...")
        generate_problems(
            args.generator_path, str(level_dir),
            args.num_problems_per_level,
            level, level,  # min_blocks == max_blocks == level -> fixed size
            seed_start=args.seed_start + level * 1000,
        )
    else:
        print(f"    Reusing cached problems for level={level} blocks ({level_dir})")

    return load_problems_from_dir(
        str(level_dir), args.domain_path,
        args.num_problems_per_level,
        max_actions=max_actions,
    )


# =====================================================================
# Evaluation
# =====================================================================

def evaluate_model_on_problems(
    train_args: argparse.Namespace,
    student_policy: torch.nn.Module,
    student_solver: ProblemSolver,
    problems: list,
    max_actions: int,
    device: torch.device,
    tmp_root: Path,
) -> float:
    """Run the student on a batch of problems and return the success rate.

    Uses a throwaway StudentTrainer instance (pointed at a temp folder) purely
    to reuse the exact solving/metrics code path used during training,
    without writing anything into the real experiment folders.
    """
    tmp_folder = Path(tempfile.mkdtemp(dir=str(tmp_root)))
    try:
        trainer = StudentTrainer(train_args, tmp_folder, student_solver, student_policy, device)
        with torch.no_grad():
            _, test_info, _, _ = trainer._solve_and_collect_trajectories(problems, max_actions)
        test_metrics = trainer.log_metrics('test', 0, test_info)
        trainer.close_writers()
        return float(test_metrics['Success rate'])
    finally:
        shutil.rmtree(tmp_folder, ignore_errors=True)


# =====================================================================
# Main
# =====================================================================

def main():
    args = parse_arguments()
    device = torch.device('cuda' if args.device == 'gpu' else 'cpu')

    experiments_dir = Path(args.experiments_dir)
    Path(args.output_plot).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output_csv).parent.mkdir(parents=True, exist_ok=True)
    tmp_root = Path(tempfile.mkdtemp(prefix='eval_by_level_'))

    levels = list(range(args.min_blocks, args.max_blocks + 1))

    print(f"\n{'='*70}")
    print(f"Discovering experiments in {experiments_dir}")
    print(f"{'='*70}\n")
    experiment_dirs = discover_experiments(experiments_dir, args.include_experiment_ids)
    print(f"\nFound {len(experiment_dirs)} candidate experiment(s)\n")

    # ---- Pre-generate / load test problems for every level once ----
    print(f"{'='*70}")
    print(f"Preparing test problems for levels {levels[0]}..{levels[-1]} blocks")
    print(f"{'='*70}\n")

    level_problems: Dict[int, list] = {}
    level_max_actions: Dict[int, int] = {}
    for level in levels:
        max_actions = max(args.max_actions_min, int(args.max_actions_factor * (level - 1)))
        level_max_actions[level] = max_actions
        try:
            level_problems[level] = get_level_problems(level, args, max_actions)
        except Exception as e:
            print(f"  Warning: failed to prepare problems for level={level}: {e}")
            level_problems[level] = []

    # ---- Evaluate every model on every level ----
    print(f"\n{'='*70}")
    print(f"Evaluating {len(experiment_dirs)} model(s) on {len(levels)} level(s)")
    print(f"{'='*70}\n")

    # results[level] -> list of (experiment_id, success_rate)
    results: Dict[int, List[Tuple[str, float]]] = defaultdict(list)

    for exp_dir in experiment_dirs:
        print(f"\033[1m\033[94mModel: {exp_dir.name}\033[0m")
        try:
            loaded = load_student_model(exp_dir, args.domain_path, device)
        except Exception:
            print(f"  Failed to load model, skipping:")
            traceback.print_exc()
            continue

        if loaded is None:
            continue
        train_args, student_policy, student_solver, last_it = loaded
        print(f"  Loaded checkpoint at iteration {last_it}")

        for level in levels:
            problems = level_problems.get(level, [])
            if not problems:
                continue
            try:
                success_rate = evaluate_model_on_problems(
                    train_args, student_policy, student_solver,
                    problems, level_max_actions[level], device, tmp_root,
                )
            except Exception:
                print(f"  Level {level}: evaluation failed:")
                traceback.print_exc()
                continue

            results[level].append((exp_dir.name, success_rate))
            print(f"  Level {level:2d} blocks: success={success_rate:.1%} "
                  f"({len(problems)} problems)")

    shutil.rmtree(tmp_root, ignore_errors=True)

    # ---- Aggregate ----
    print(f"\n{'='*70}")
    print(f"Aggregating results")
    print(f"{'='*70}\n")

    agg_levels, agg_mean, agg_std, agg_n = [], [], [], []
    csv_rows = ["level,experiment_id,success_rate"]
    for level in levels:
        entries = results.get(level, [])
        if not entries:
            continue
        rates = [r for _, r in entries]
        mean = sum(rates) / len(rates)
        std = (sum((r - mean) ** 2 for r in rates) / len(rates)) ** 0.5
        agg_levels.append(level)
        agg_mean.append(mean)
        agg_std.append(std)
        agg_n.append(len(rates))
        for exp_id, r in entries:
            csv_rows.append(f"{level},{exp_id},{r:.6f}")
        print(f"  Level {level:2d}: mean success={mean:.1%}  std={std:.1%}  n_models={len(rates)}")

    with open(args.output_csv, 'w') as f:
        f.write("\n".join(csv_rows) + "\n")
    print(f"\nRaw per-model results written to {args.output_csv}")

    # ---- Plot ----
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.errorbar(
        agg_levels, agg_mean, yerr=agg_std,
        marker='o', markersize=4, capsize=3, linewidth=1.5,
        label=f"Mean over {max(agg_n) if agg_n else 0} model(s)",
    )
    ax.set_xlabel("Difficulty level (number of blocks)")
    ax.set_ylabel("Mean success rate")
    ax.set_ylim(-0.05, 1.05)
    ax.set_title("Student success rate vs. blocksworld difficulty level")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(args.output_plot, dpi=150)
    print(f"Plot written to {args.output_plot}")


if __name__ == '__main__':
    main()