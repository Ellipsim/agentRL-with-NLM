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
# Run tests
pytest tests/ -v

# Run specific test category
pytest -m ppo -v
pytest -m loading -v
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

## Author

jrdominguez

## License

MIT
EOF
