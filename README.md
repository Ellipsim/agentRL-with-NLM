# Training Scripts — AgentRL PDDL Solver

This document covers the two training scripts available for training the PPO solver policy.

---

## Scripts Overview

| Script | Module | Description |
|--------|--------|-------------|
| `train_and_test.py` | `src.agent.controller.train_and_test` | Standard training with fixed problem sets |
| `train_and_test_ACG.py` | `src.agent.controller.train_and_test_ACG` | Automatic Curriculum Generation (ACG) with progressive difficulty |

---

## Training Without Curriculum (`train_and_test.py`)

Standard training loop. Requires pre-generated problem sets for train, validation, and test splits. Selects the best checkpoint based on validation performance.

### Usage

```bash
python -m src.agent.controller.train_and_test \
    --domain-path data/domains/blocksworld.pddl \
    --train-problems-dir data/problems/train \
    --val-problems-dir data/problems/val \
    --test-problems-dir data/problems/test \
    --device gpu \
    --seed 1 \
    --steps 200 \
    --num-problems-train 30 \
    --num-problems-val 100 \
    --num-problems-test 100 \
    --max-actions-train 116 \
    --max-actions-val 116 \
    --max-actions-test 116 \
    --val-period 20 \
    --log-period 1 \
    --batch-size 32 \
    --disc-factor 0.99 \
    --gae-factor 0.95 \
    --train-mode supersede \
    --test-mode supersede
```

> **Note:** The maximum number of actions needed to solve a Blocksworld problem with N blocks is `4 * (N - 1)`.

### Key Arguments

#### Domain & Problems
| Argument | Default | Description |
|----------|---------|-------------|
| `--domain-path` | required | Path to `domain.pddl` |
| `--train-problems-dir` | required | Directory with training `.pddl` files |
| `--val-problems-dir` | required | Directory with validation `.pddl` files |
| `--test-problems-dir` | required | Directory with test `.pddl` files |

#### Training
| Argument | Default | Description |
|----------|---------|-------------|
| `--steps` | 100 | Total training iterations |
| `--num-problems-train` | 5 | Problems solved per iteration |
| `--max-actions-train` | 50 | Action budget per training problem |
| `--batch-size` | 32 | PPO minibatch size |
| `--min-samples-train` | 10 | Min trajectory samples before a PPO update |
| `--grad-clip` | 0.5 | Gradient clipping (`-1` to disable) |
| `--disc-factor` | 0.99 | Discount factor γ |
| `--gae-factor` | 0.95 | GAE factor λ |

#### Validation
| Argument | Default | Description |
|----------|---------|-------------|
| `--val-period` | 10 | Steps between validation runs |
| `--num-problems-val` | 10 | Problems per validation epoch |
| `--max-actions-val` | 50 | Action budget per validation problem |

#### Testing
| Argument | Default | Description |
|----------|---------|-------------|
| `--num-problems-test` | 20 | Problems per test run |
| `--max-actions-test` | 50 | Action budget per test problem |

#### Modes
| Argument | Options | Description |
|----------|---------|-------------|
| `--train-mode` | `resume` / `supersede` / `skip` | Resume continues from last checkpoint; supersede restarts from scratch |
| `--test-mode` | `missing` / `supersede` / `skip` | Controls the final test run |

#### Rewards
| Argument | Default | Description |
|----------|---------|-------------|
| `--reward-goal-reached` | 1.0 | Bonus reward when goal is reached |
| `--reward-step` | -0.01 | Penalty per action step |
| `--reward-efficiency` | 0.5 | Weight for efficiency bonus at episode end |

---

## Training With Curriculum (`train_and_test_ACG.py`)

Automatic Curriculum Generation training loop. Problems are generated on-the-fly with increasing difficulty. The agent must reach a configurable success threshold before advancing to the next difficulty level. Includes experience replay to prevent forgetting.

### Usage

```bash
python -m src.agent.controller.train_and_test_ACG \
    --domain-path data/domains/blocksworld.pddl \
    --device gpu \
    --seed 1 \
    --steps 200 \
    --num-problems-train 20 \
    --num-problems-test 100 \
    --test-period 20 \
    --check-advance-period 5 \
    --advance-threshold 0.8 \
    --max-levels 20 \
    --min-blocks-start 2 \
    --max-blocks-start 3 \
    --blocks-increment 1 \
    --log-period 1 \
    --batch-size 32 \
    --replay-prob 0.3 \
    --replay-buffer-size 500 \
    --train-mode supersede \
    --test-mode supersede
```

### Key Arguments

#### Domain & Problem Generation
| Argument | Default | Description |
|----------|---------|-------------|
| `--domain-path` | required | Path to `domain.pddl` |
| `--generator-path` | `./problem_generator/.../blocksworld` | Path to the blocksworld generator binary |
| `--data-dir` | `./data/problems/curriculum` | Directory where generated problems are stored |

#### Curriculum Configuration
| Argument | Default | Description |
|----------|---------|-------------|
| `--min-blocks-start` | 2 | Minimum blocks at level 1 |
| `--max-blocks-start` | 3 | Maximum blocks at level 1 |
| `--blocks-increment` | 1 | Blocks added per level |
| `--max-levels` | 4 | Total number of curriculum levels |
| `--advance-threshold` | 0.8 | Success rate required to advance to the next level |
| `--check-advance-period` | 10 | How often (in steps) to check if ready to advance |
| `--target-success-rate` | 1.0 | Stop training early if test success rate reaches this value |
| `--test-min-blocks` | level 1 min | Min blocks for the fixed test set |
| `--test-max-blocks` | hardest level max | Max blocks for the fixed test set |

#### Training
| Argument | Default | Description |
|----------|---------|-------------|
| `--steps` | 100 | Total training iterations |
| `--num-problems-train` | 5 | Problems solved per iteration |
| `--max-actions-train` | auto | Action budget per training problem (defaults to `4 * (max_blocks - 1)`) |
| `--batch-size` | 32 | PPO minibatch size |
| `--min-samples-train` | 10 | Min trajectory samples before a PPO update |
| `--grad-clip` | 0.5 | Gradient clipping (`-1` to disable) |
| `--disc-factor` | 0.99 | Discount factor γ |
| `--gae-factor` | 0.95 | GAE factor λ |

#### Periodic Test Evaluation
| Argument | Default | Description |
|----------|---------|-------------|
| `--test-period` | 10 | Steps between test evaluations (`-1` = only at end) |
| `--num-problems-test` | 20 | Problems per test evaluation |
| `--max-actions-test` | auto | Action budget per test problem |

#### Experience Replay
| Argument | Default | Description |
|----------|---------|-------------|
| `--replay-prob` | 0.2 | Probability of replacing a training slot with a replayed problem (`0.0` to disable) |
| `--replay-buffer-size` | 3000 | Max problems stored in the replay buffer (FIFO eviction) |

#### Offline Evaluation
| Argument | Default | Description |
|----------|---------|-------------|
| `--save-level-checkpoints` | False | Save a checkpoint each time the curriculum advances a level, for later offline evaluation |

#### Modes & Rewards
Same as `train_and_test.py` — see the tables above.

---

## Offline Per-Level Evaluation

When training with `--save-level-checkpoints`, you can run a full per-level evaluation after training without slowing down the training run:

```bash
python -m src.scripts.evaluate_policy_per_level \
    --experiment-id <id> \
    --domain-path data/domains/blocksworld.pddl \
    --num-problems-per-level 50
```

This will discover all saved level-advance checkpoints, evaluate each one across all difficulty levels, and produce:
- One JSON + three-panel plot per checkpoint
- A single combined `all_advance_evals.png` showing success rate progression across all curriculum advances

Use `--force-reeval` to re-evaluate checkpoints that already have saved results.

---

## Experiment Management

Both scripts generate a unique experiment ID based on the argument hash and store all outputs under `./experiments/<experiment_id>/`:

```
experiments/<id>/
├── experiment_info.json       # All hyperparameters and metadata
├── checkpoints/
│   ├── last.ckpt              # Latest checkpoint
│   ├── best.ckpt              # Best checkpoint (train_and_test.py only)
│   └── level_advances/        # Per-level checkpoints (ACG only, with --save-level-checkpoints)
├── logs/                      # TensorBoard logs
└── test/                      # Final test results
```

---

## Reproducibility

Both scripts accept `--seed` and `--run-id`. Use `--run-id` to repeat an experiment with identical hyperparameters while producing a different experiment ID:

```bash
# Run experiment 3 times
python -m src.agent.controller.train_and_test_ACG --seed 1 --run-id 0 ...
python -m src.agent.controller.train_and_test_ACG --seed 1 --run-id 1 ...
python -m src.agent.controller.train_and_test_ACG --seed 1 --run-id 2 ...
```