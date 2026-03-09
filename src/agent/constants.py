"""
> constants.py

Constants for the RL solving agent.
Kept separate from the NeSIG constants.py to avoid importing
generation-specific dependencies (consistency evaluators, etc.)
that are not needed for solving.
"""

from pathlib import Path

# Path to the blocksworld domain PDDL file
BLOCKSWORLD_DOMAIN_PATH = Path('data/domains/blocks-domain.pddl')

# Domain info for the solver — no consistency evaluator needed
SOLVER_DOMAIN_INFO = {
    'blocksworld': {
        'path': BLOCKSWORLD_DOMAIN_PATH,
        'goal_predicates': (('on', ('block', 'block')),),
    },
}