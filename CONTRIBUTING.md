# Contributing to C++ Function Grouper

Thank you for your interest in contributing to the C++ Function Grouper! This document provides guidelines and workflows for developing this project.

## Table of Contents

- [Development Philosophy](#development-philosophy)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Code Quality Standards](#code-quality-standards)
- [Testing Requirements](#testing-requirements)
- [Constitution Compliance](#constitution-compliance)
- [Pull Request Process](#pull-request-process)

## Development Philosophy

This project follows a **Test-Driven Development (TDD)** approach and adheres to strict quality standards defined in our [Project Constitution](.specify/memory/constitution.md). All contributions must:

1. Write tests **BEFORE** writing implementation code
2. Pass all quality gates (linting, type checking, tests)
3. Meet performance requirements
4. Include comprehensive documentation

## Getting Started

### Prerequisites

- **Python 3.11 or later**
- **uv** package manager (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Git** for version control
- Basic understanding of Python, C++, and graph algorithms

### Initial Setup

```bash
# Clone the repository
git clone https://github.com/your-org/cpp-dependency-analysis.git
cd cpp-dependency-analysis

# Sync dependencies with uv
uv sync

# Verify installation
uv run function-grouper --help
```

## Development Workflow

### 1. Red-Green-Refactor (TDD Cycle)

#### RED: Write Failing Test First

```python
# tests/unit/test_new_feature.py
def test_new_feature():
    """Test description."""
    result = some_function()
    assert result == expected_value
    # This test MUST fail initially
```

Run the test to verify it fails:
```bash
uv run pytest tests/unit/test_new_feature.py -v
```

#### GREEN: Write Minimum Code to Pass

```python
# src/function_grouper/module.py
def some_function():
    """Minimum implementation to pass test."""
    return expected_value
```

Run the test to verify it passes:
```bash
uv run pytest tests/unit/test_new_feature.py -v
```

#### REFACTOR: Improve Code Quality

- Clean up code structure
- Add comprehensive type hints
- Improve naming and readability
- Optimize performance if needed
- Ensure all quality gates pass

### 2. Quality Gates

Before committing, ensure all quality gates pass:

```bash
# Run linter (zero warnings required)
uv run ruff check src/ tests/

# Run type checker (strict mode)
uv run mypy src/function_grouper

# Run all tests with coverage (>90% required)
uv run pytest --cov=src/function_grouper --cov-report=term-missing

# Run the full test suite
uv run pytest
```

### 3. Commit Guidelines

- Write clear, concise commit messages (<80 words)
- Reference issue numbers when applicable
- Follow conventional commits format: `type(scope): description`
- Examples:
  - `feat(parser): add support for C++20 concepts`
  - `fix(grouper): handle empty call graphs correctly`
  - `docs(readme): update installation instructions`
  - `test(analyzer): add edge case for circular dependencies`

## Code Quality Standards

### Python Code Style

- **Line length**: Maximum 100 characters
- **Target version**: Python 3.11+
- **Linter**: ruff with default rules (pycodestyle, pyflakes, isort, flake8-bugbear)
- **Formatter**: Follow PEP 8 conventions

### Type Hints

All code must include comprehensive type hints:

```python
from typing import List, Dict, Optional
from function_grouper.models.function import Function

def analyze_functions(
    functions: List[Function],
    include_templates: bool = True
) -> Dict[str, List[str]]:
    """Analyze functions and return groups.

    Args:
        functions: List of Function objects to analyze
        include_templates: Whether to include template functions

    Returns:
        Dictionary mapping group IDs to function names
    """
    ...
```

### Documentation

- All modules, classes, and public functions must have docstrings
- Use Google-style docstrings
- Include examples for complex functionality
- Keep README.md synchronized with code changes

## Testing Requirements

### Test Coverage

- **Minimum coverage**: 90% for all production code
- **Required test types**:
  - Unit tests for all components
  - Integration tests for end-to-end workflows
  - Contract tests for CLI interface
  - Performance benchmarks for critical paths

### Test Organization

```
tests/
├── unit/                    # Fast, isolated component tests
│   ├── test_parser.py
│   ├── test_analyzer.py
│   ├── test_grouper.py
│   └── test_formatters.py
├── integration/             # End-to-end workflow tests
│   ├── test_end_to_end.py
│   └── fixtures/           # Sample C++ files for testing
│       ├── simple_independent.cpp
│       ├── complex_dependencies.cpp
│       └── circular_deps.cpp
└── contract/                # CLI and output format tests
    ├── test_cli_interface.py
    └── test_output_formats.py
```

### Writing Tests

```python
import pytest
from function_grouper.parser.cpp_parser import CppParser

def test_parse_free_function():
    """Test parsing a simple free function."""
    code = """
    void hello() {
        // Empty function
    }
    """
    parser = CppParser()
    functions = parser.parse_string(code, "test.cpp")

    assert len(functions) == 1
    assert functions[0].name == "hello"

@pytest.mark.slow
def test_large_file_performance():
    """Test parsing performance on large files."""
    # Use pytest-benchmark for performance tests
    ...
```

## Constitution Compliance

This project follows **Constitution v1.1.0** with 9 core principles:

### I. Zero-Defect Commitment
- No known bugs in production code
- All tests must pass before merging
- Fix bugs immediately when discovered

### II. Test-Driven Development (TDD)
- ✅ **REQUIRED**: Write tests BEFORE implementation
- Follow Red-Green-Refactor cycle
- Never skip testing

### III. Code Quality Standards
- ✅ Zero warnings from ruff
- ✅ Zero errors from mypy (strict mode)
- ✅ >90% test coverage

### IV. Static Analysis First
- Run linters before commits
- Address all type checker warnings
- Use automated quality tools

### V. Memory Safety
- Use Python's automatic memory management
- Profile memory usage for large files
- Target: <2GB memory with 1000 functions

### VI. Build Verification
- ✅ CI/CD pipeline must pass
- All quality gates automated
- Pre-commit hooks enforce standards

### VII. Dependency Hygiene
- Pin dependency versions
- Regular security audits
- Minimal dependency footprint

### VIII. Comprehensive Documentation
- ✅ README with verified runnable samples
- ✅ All examples in [examples/](examples/) directory
- ✅ Troubleshooting guide included

### IX. Sample-Driven Verification
- ✅ All features demonstrated with working examples
- ✅ Samples verified before releases
- ✅ Examples tested in CI pipeline

## Pull Request Process

### 1. Create Feature Branch

```bash
git checkout -b feature/my-new-feature
```

### 2. Develop Following TDD

- Write tests first
- Implement minimum code
- Refactor and improve
- Run quality gates

### 3. Update Documentation

- Add/update docstrings
- Update README if needed
- Add examples if applicable
- Update CHANGELOG

### 4. Run Complete Verification

```bash
# Run all quality checks
uv run ruff check src/ tests/
uv run mypy src/function_grouper
uv run pytest --cov=src/function_grouper

# Verify examples still work
uv run function-grouper examples/simple.cpp
uv run function-grouper examples/complex.cpp -f json
```

### 5. Submit Pull Request

- Provide clear description of changes
- Reference related issues
- Include test results
- Ensure CI pipeline passes

### 6. Code Review

- Address reviewer feedback
- Update tests/code as needed
- Maintain quality standards
- Re-run quality gates after changes

## Performance Requirements

All features must meet these performance targets:

- **Parse speed**: Process 10,000-line files in <30 seconds
- **Memory usage**: <2GB with 1,000 function definitions
- **Parse success rate**: 95%+ for valid C++ code

Run benchmarks:
```bash
uv run pytest -m benchmark --benchmark-only
```

## Getting Help

- **Specification**: [specs/001-function-grouper/spec.md](specs/001-function-grouper/spec.md)
- **Data Models**: [specs/001-function-grouper/data-model.md](specs/001-function-grouper/data-model.md)
- **CLI Contract**: [specs/001-function-grouper/contracts/cli-interface.md](specs/001-function-grouper/contracts/cli-interface.md)
- **Research Notes**: [specs/001-function-grouper/research.md](specs/001-function-grouper/research.md)
- **Quickstart Guide**: [specs/001-function-grouper/quickstart.md](specs/001-function-grouper/quickstart.md)

## Resources

- [libclang Python API](https://github.com/llvm/llvm-project/tree/main/clang/bindings/python)
- [Click Documentation](https://click.palletsprojects.com)
- [NetworkX Documentation](https://networkx.org/documentation/stable/)
- [pytest Documentation](https://docs.pytest.org)
- [uv Documentation](https://docs.astral.sh/uv/)

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

Thank you for contributing! 🎉
