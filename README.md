# AgentRL - PDDL Solver with PPO

A reinforcement learning agent for solving PDDL planning problems using PPO (Proximal Policy Optimization).

## Features

- **PDDL Problem Solver**: Load and solve PDDL blocksworld problems
- **PPO Policy**: Trained policy using Proximal Policy Optimization
- **Neural Network**: NLM (Neural Logic Machine) for action prediction
- **Comprehensive Tests**: Full test suite for all components

## Installation
```bash
conda create -n agentRL python=3.8
conda activate agentRL
pip install -r requirements.txt
```

## Usage
```bash
python -m src.agent.controller.train_and_test \
  --domain-path data/domains/blocksworld.pddl \
  --train-problems-dir data/problems/train \
  --val-problems-dir data/problems/val \
  --test-problems-dir data/problems/test \
  --steps 100 \
  --policy-type PPO \
  --device gpu
```

## **Key Arguments:**
```
Domain & Problems:
  --domain-path           Path to domain.pddl
  --train-problems-dir    Training problems folder
  --val-problems-dir      Validation problems folder
  --test-problems-dir     Test problems folder

Training:
  --steps                 Number of iterations (default: 100)
  --num-problems-train    Problems per iteration (default: 5)
  --max-actions-train     Action budget (default: 50)
  --batch-size            PPO batch size (default: 32)
  --solve-PPO-epochs      PPO epochs (default: 3)

Validation:
  --val-period            Steps between validation (default: 10)
  --num-problems-val      Val problems per epoch (default: 10)

Testing:
  --num-problems-test     Test problems (default: 20)

Modes:
  --train-mode            skip/supersede/resume (default: resume)
  --test-mode             skip/supersede/missing (default: missing)

Rewards:
  --reward-goal-reached   Goal bonus (default: 1.0)
  --reward-step           Step penalty (default: -0.01)
  --reward-efficiency     Efficiency weight (default: 0.5)
```

## Project Structure
```
agentRL/
├── src/
│   └── agent/
│       ├── pddl/
│       │   ├── pddl_problem.py
│       │   └── pddl_state.py
│       └── learning/
│           ├── generative_policy.py
│           ├── model_wrapper.py
│           └── solver_policy.py
├── tests/
│   ├── conftest.py
│   ├── test_problem_loading.py
│   ├── test_problem_state.py
│   ├── test_problem_actions.py
│   ├── test_problem_solving.py
│   ├── test_solver_random_policy.py
│   └── test_ppo_solver_policy.py
├── data/
│   ├── domains/
│   └── problems/
└── pyproject.toml
```

## Tests

- `test_problem_loading.py`: Loading PDDL problems
- `test_problem_state.py`: Problem state management
- `test_problem_actions.py`: Action applicability and execution
- `test_problem_solving.py`: Problem solving and reset
- `test_solver_random_policy.py`: Random baseline policy
- `test_ppo_solver_policy.py`: PPO policy training and inference

## Known Issues

- DuplicateConstantDefinition bug when deepcopying parser (workaround: use fresh_parser fixture)

## Future Work

- Extend to other PDDL domains beyond Blocksworld
- Implement curriculum learning
- Add visualization of problem solving trajectories

## License

MIT
EOF
