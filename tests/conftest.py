"""Pytest configuration and fixtures."""

from collections.abc import Iterator
from pathlib import Path

import pytest


@pytest.fixture
def fixtures_dir() -> Path:
    """Return the path to the test fixtures directory."""
    return Path(__file__).parent / "integration" / "fixtures"


@pytest.fixture
def simple_independent_cpp(fixtures_dir: Path) -> Path:
    """Return path to simple_independent.cpp fixture."""
    return fixtures_dir / "simple_independent.cpp"


@pytest.fixture
def complex_dependencies_cpp(fixtures_dir: Path) -> Path:
    """Return path to complex_dependencies.cpp fixture."""
    return fixtures_dir / "complex_dependencies.cpp"


@pytest.fixture
def circular_deps_cpp(fixtures_dir: Path) -> Path:
    """Return path to circular_deps.cpp fixture."""
    return fixtures_dir / "circular_deps.cpp"


@pytest.fixture
def temp_cpp_file(tmp_path: Path) -> Iterator[Path]:
    """Create a temporary C++ file for testing."""
    cpp_file = tmp_path / "test.cpp"
    yield cpp_file
    # Cleanup happens automatically with tmp_path
