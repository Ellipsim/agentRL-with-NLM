"""
> constants.py

Constants for the RL solving agent.
Kept separate from the NeSIG constants.py to avoid importing
generation-specific dependencies (consistency evaluators, etc.)
that are not needed for solving.
"""

from pathlib import Path
import shutil
import errno

# Path to the blocksworld domain PDDL file
BLOCKSWORLD_DOMAIN_PATH = Path('data/domains/blocks-domain.pddl')

# Domain info for the solver — no consistency evaluator needed
SOLVER_DOMAIN_INFO = {
    'blocksworld': {
        'path': BLOCKSWORLD_DOMAIN_PATH,
        'goal_predicates': (('on', ('block', 'block')),),
    },
}

# Get base path
BASE_PATH = Path(__file__).parent.parent.parent

# Experiment storage
EXPERIMENTS_PATH = BASE_PATH / "experiments"

# Folder and file names
EXPERIMENT_INFO_FILENAME = "experiment_info.json"
LOGS_FOLDER_NAME = "logs"
CKPTS_FOLDER_NAME = "checkpoints"
VAL_FOLDER_NAME = "validation"
TEST_FOLDER_NAME = "test"

# ID generation
ID_LENGTH = 8

# Additional experiment info to save
ADDITIONAL_EXPERIMENT_INFO = {
    "created_with": "AgentRL Solver",
    "version": "1.0",
}


def remove_if_exists(path):
    """Remove a file or directory if it exists."""
    try:
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
    except FileNotFoundError:
        pass
    except OSError as e:
        if e.errno != errno.ENOENT:
            raise

# TEST AND TRAIN
EXCLUDED_ARGS_ID = {'seed', 'run_id', 'train_mode', 'test_mode', 'raise_error_test',
                    'log_period', 'device', 'experiments_dir'}
ID_LENGTH = 8
ADDITIONAL_EXPERIMENT_INFO = {}

# Replay buffer
REPLAY_BUFFER_FILENAME = 'replay_buffer.json'