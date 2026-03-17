"""
> conftest.py

Shared fixtures and configuration for all tests.
Automatically discovers and parametrizes all .pddl files in data/problems/

Use:
    #Fast - Only 5 problems
    pytest --fast

    #Specific number
    pytest --max-problems 20
    
    # Full suite
    pytest


"""
import pytest
from pathlib import Path
from lifted_pddl import Parser


@pytest.fixture(scope="session")
def data_dir():
    """Return path to the data directory."""
    return Path(__file__).parent.parent / "data"


@pytest.fixture(scope="session")
def domain_file(data_dir):
    """Return path to the blocksworld domain."""
    return data_dir / "domains" / "blocksworld.pddl"


@pytest.fixture
def parser(domain_file):
    """A Parser already loaded with the blocksworld domain."""
    p = Parser()
    p.parse_domain(str(domain_file))
    return p

@pytest.fixture
def fresh_parser(domain_file):
    """Return a function that creates fresh parsers with cleared language state."""
    def _create_parser():
        p = Parser()
        p.parse_domain(str(domain_file))
        return p
    return _create_parser

def pytest_addoption(parser):
    parser.addoption(
        "--fast", action="store_true", default=False,
        help="Run only a small subset of problems for fast testing"
    )
    parser.addoption(
        "--max-problems", type=int, default=None,
        help="Maximum number of problem files to test"
    )


def pytest_generate_tests(metafunc):
    """Automatically parametrize tests that use problem_file fixture."""
    if "problem_file" in metafunc.fixturenames:
        data_dir = Path(__file__).parent.parent / "data"
        problems_dir = data_dir / "problems"
        problem_files = sorted(problems_dir.glob("**/*.pddl"))

        if not problem_files:
            pytest.skip(f"No .pddl files found in {problems_dir}")

        # Limit problems based on flags
        fast = metafunc.config.getoption("--fast", default=False)
        max_problems = metafunc.config.getoption("--max-problems", default=None)

        if fast:
            problem_files = problem_files[:5]
        elif max_problems is not None:
            problem_files = problem_files[:max_problems]

        metafunc.parametrize(
            "problem_file",
            problem_files,
            ids=[f.stem for f in problem_files],
        )