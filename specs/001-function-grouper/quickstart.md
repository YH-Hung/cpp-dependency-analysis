# Quickstart Guide: C++ Function Grouper

## Overview

This guide helps you get started with developing the C++ Function Grouper tool from specification to implementation. Follow these steps to set up your environment, understand the architecture, and begin coding.

## Prerequisites

Before starting, ensure you have:

- **Python 3.11 or later** installed
- **uv** package manager installed (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- **Git** for version control
- Basic understanding of Python, C++, and graph algorithms
- Familiarity with AST concepts

## Project Setup

### 1. Initialize the Project with uv

```bash
# Navigate to repository root
cd cpp-dependency-analysis

# Initialize uv project
uv init --name function-grouper --python 3.11

# This creates:
# - pyproject.toml
# - .python-version
# - src/function_grouper/
```

### 2. Configure pyproject.toml

Edit `pyproject.toml` to include dependencies:

```toml
[project]
name = "function-grouper"
version = "0.1.0"
description = "Analyze C++ function dependencies and identify independent groups"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "libclang>=18.1.1",
    "click>=8.1.0",
    "networkx>=3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-cov>=4.1.0",
    "pytest-benchmark>=4.0.0",
    "mypy>=1.7.0",
    "ruff>=0.1.0",
    "memory-profiler>=0.61.0",
]

[project.scripts]
function-grouper = "function_grouper.cli.main:main"

[tool.ruff]
line-length = 100
target-version = "py311"

[tool.mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-v --cov=src/function_grouper --cov-report=term-missing"
```

### 3. Install Dependencies

```bash
# Install project with dev dependencies
uv pip install -e ".[dev]"

# Verify installation
python -c "import clang.cindex; print('libclang installed successfully')"
```

## Architecture Overview

The tool consists of five main components:

```
┌─────────────┐
│  CLI Layer  │  User interface, argument parsing, progress display
└──────┬──────┘
       │
┌──────▼──────┐
│   Parser    │  libclang integration, AST traversal, function extraction
└──────┬──────┘
       │
┌──────▼──────┐
│  Analyzer   │  Call graph construction, dependency analysis
└──────┬──────┘
       │
┌──────▼──────┐
│   Grouper   │  Connected components, independence detection
└──────┬──────┘
       │
┌──────▼──────┐
│ Formatters  │  JSON, text, DOT output generation
└─────────────┘
```

## Development Workflow (TDD)

Following the constitution's TDD requirement:

### Step 1: Write Failing Tests FIRST

```python
# tests/unit/test_parser.py

import pytest
from function_grouper.parser.cpp_parser import CppParser
from function_grouper.models.function import Function, FunctionKind

def test_parse_simple_function():
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
    assert functions[0].kind == FunctionKind.FREE_FUNCTION
    # THIS TEST WILL FAIL - implementation doesn't exist yet
```

### Step 2: Run Tests (Verify Failure)

```bash
pytest tests/unit/test_parser.py -v

# Expected output:
# FAILED tests/unit/test_parser.py::test_parse_simple_function
# ModuleNotFoundError: No module named 'function_grouper.parser.cpp_parser'
```

### Step 3: Implement Minimum Code

```python
# src/function_grouper/parser/cpp_parser.py

from typing import List
from clang.cindex import Index, CursorKind
from function_grouper.models.function import Function, FunctionKind

class CppParser:
    def __init__(self):
        self.index = Index.create()

    def parse_string(self, code: str, filename: str) -> List[Function]:
        """Parse C++ code string and extract functions."""
        # Create temporary file with code
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.cpp', delete=False) as f:
            f.write(code)
            temp_path = f.name

        try:
            tu = self.index.parse(temp_path, args=['-std=c++17'])
            functions = []

            def traverse(node):
                if node.kind == CursorKind.FUNCTION_DECL:
                    func = Function(
                        name=node.spelling,
                        qualified_name=node.spelling,  # Simplified for now
                        signature=node.displayname,
                        location=...,  # To be implemented
                        kind=FunctionKind.FREE_FUNCTION,  # Simplified
                        calls=[],  # To be implemented
                        parse_status="SUCCESS"
                    )
                    functions.append(func)

                for child in node.get_children():
                    traverse(child)

            traverse(tu.cursor)
            return functions
        finally:
            import os
            os.unlink(temp_path)
```

### Step 4: Run Tests Again (Green)

```bash
pytest tests/unit/test_parser.py -v

# Expected output:
# PASSED tests/unit/test_parser.py::test_parse_simple_function
```

### Step 5: Refactor

Clean up code, improve structure, add type hints, ensure quality.

### Step 6: Add More Tests

Continue the cycle for each new feature:
- Function calls detection
- Member function handling
- Template function support
- Error handling
- etc.

## Key Implementation Milestones

### Milestone 1: Basic Parsing

**Goal**: Parse a C++ file and extract function names

**Tests**:
- `test_parse_free_function()`
- `test_parse_member_function()`
- `test_parse_multiple_functions()`

**Implementation**: `CppParser` class using libclang

### Milestone 2: Call Detection

**Goal**: Identify function call relationships

**Tests**:
- `test_detect_function_call()`
- `test_detect_multiple_calls()`
- `test_ignore_external_calls()`

**Implementation**: Extend `CppParser` to traverse `CALL_EXPR` nodes

### Milestone 3: Graph Construction

**Goal**: Build directed graph of function dependencies

**Tests**:
- `test_build_call_graph()`
- `test_add_function_node()`
- `test_add_call_edge()`

**Implementation**: `CallGraph` class using networkx

### Milestone 4: Grouping Logic

**Goal**: Find connected components (independent groups)

**Tests**:
- `test_find_independent_groups()`
- `test_identify_circular_dependencies()`
- `test_group_independence_flag()`

**Implementation**: Use `networkx.connected_components()`

### Milestone 5: Output Formatting

**Goal**: Generate JSON, text, and DOT outputs

**Tests**:
- `test_json_formatter()`
- `test_text_formatter()`
- `test_dot_formatter()`
- `test_json_schema_compliance()`

**Implementation**: Formatter classes for each format

### Milestone 6: CLI Integration

**Goal**: Complete command-line interface

**Tests**:
- `test_cli_help()`
- `test_cli_basic_usage()`
- `test_cli_output_formats()`
- `test_cli_error_handling()`

**Implementation**: `click` application in `cli/main.py`

### Milestone 7: Performance & Polish

**Goal**: Meet performance requirements (10k lines in 30s)

**Tests**:
- `test_large_file_performance()`
- `test_memory_usage_limit()`
- `test_progress_indication()`

**Implementation**: Optimization, profiling, progress bars

## Running Quality Checks

### Linting

```bash
# Run ruff linter
ruff check src/ tests/

# Auto-fix issues
ruff check --fix src/ tests/
```

### Type Checking

```bash
# Run mypy type checker
mypy src/function_grouper
```

### Test Coverage

```bash
# Run tests with coverage report
pytest --cov=src/function_grouper --cov-report=html

# View coverage in browser
open htmlcov/index.html
```

### Performance Profiling

```bash
# Memory profiling
mprof run function-grouper large_file.cpp
mprof plot

# Time profiling
python -m cProfile -o profile.stats -m function_grouper.cli.main large_file.cpp
python -m pstats profile.stats
```

## Example Test Fixtures

Create realistic C++ test files in `tests/integration/fixtures/`:

### simple_independent.cpp
```cpp
void functionA() {
    // Independent
}

void functionB() {
    // Independent
}

void functionC() {
    // Independent
}
```

### complex_dependencies.cpp
```cpp
void helper() {}

void process() {
    helper();
}

void analyze() {
    process();
    helper();
}

void independentFunction() {
    // Separate group
}
```

### circular_deps.cpp
```cpp
void funcA();
void funcB();

void funcA() {
    funcB();
}

void funcB() {
    funcA();
}
```

## Common Development Tasks

### Add a New Feature

1. Write user story and acceptance criteria in spec.md
2. Write failing integration test
3. Write failing unit tests for components
4. Implement minimum code to pass tests
5. Refactor and optimize
6. Update documentation
7. Run full quality checks

### Debug Parsing Issues

```python
# Enable libclang diagnostics
tu = index.parse('file.cpp', args=['-std=c++17'])
for diag in tu.diagnostics:
    print(f"{diag.severity}: {diag.spelling}")
    print(f"  Location: {diag.location}")
```

### Test with Real C++ Projects

```bash
# Test against open-source C++ projects
git clone https://github.com/nlohmann/json.git
function-grouper json/src/json.cpp -f json -o results.json

# Verify accuracy manually
cat results.json | jq '.metadata'
```

## Next Steps

1. **Read the Research**: Review `research.md` for libclang API details
2. **Understand Data Model**: Study `data-model.md` for entity relationships
3. **Review Contracts**: Check `contracts/cli-interface.md` for expected behavior
4. **Start with Tests**: Begin TDD cycle with `tests/unit/test_parser.py`
5. **Iterate**: Follow Red-Green-Refactor for each component
6. **Integration**: Connect components and test end-to-end
7. **Optimize**: Profile and improve performance to meet targets
8. **Polish**: Add progress bars, error handling, documentation

## Resources

- **libclang Python API**: [GitHub - llvm/llvm-project](https://github.com/llvm/llvm-project/tree/main/clang/bindings/python)
- **Click Documentation**: [https://click.palletsprojects.com](https://click.palletsprojects.com)
- **NetworkX Documentation**: [https://networkx.org/documentation/stable/](https://networkx.org/documentation/stable/)
- **pytest Documentation**: [https://docs.pytest.org](https://docs.pytest.org)
- **Project Constitution**: `.specify/memory/constitution.md`
- **Feature Spec**: `specs/001-function-grouper/spec.md`

## Getting Help

- Review spec.md for requirements
- Check data-model.md for entity structures
- Refer to contracts/cli-interface.md for CLI behavior
- Read research.md for implementation guidance
- Run tests frequently to catch issues early
- Use mypy and ruff to maintain code quality

Happy coding! 🚀
