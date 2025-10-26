# Implementation Plan: C++ Function Grouper

**Branch**: `001-function-grouper` | **Date**: 2025-10-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-function-grouper/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Build a CLI tool that analyzes C++ implementation files to identify independent function groups based on call relationships. The tool parses C++ source using AST-based analysis (not regex), builds a dependency graph, performs connected component analysis to find independent groups, and outputs results in multiple formats (JSON, text, DOT). Target performance: 10,000-line files in under 30 seconds with up to 1000 functions, using maximum 2GB memory.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: libclang 18.1.1+ (C++ AST parser with full C++17/C++20 support), click (CLI framework), networkx (graph algorithms)
**Package Manager**: uv (modern Python package and project manager)
**Storage**: File-based (input: .cpp files, output: JSON/text/DOT files)
**Testing**: pytest with pytest-cov for coverage, pytest-benchmark for performance testing
**Target Platform**: Cross-platform CLI (Linux, macOS, Windows)
**Project Type**: Single command-line application
**Performance Goals**:
  - Parse and analyze 10,000-line files in <30 seconds
  - Handle up to 1000 function definitions
  - Memory usage <2GB
**Constraints**:
  - Must use AST-based parsing (not regex)
  - Must handle C++17/C++20 syntax
  - Must gracefully handle parse errors (partial analysis)
  - Must provide progress indication for long operations
**Scale/Scope**:
  - Single-file analysis (no multi-file project support in MVP)
  - Handle realistic C++ codebases (10k+ lines, hundreds of functions)
  - Support three output formats (JSON, plain text, Graphviz DOT)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Note**: The constitution specifies C++ code quality standards. However, this tool is written in Python to analyze C++ code. The following gates apply with Python-specific adaptations:

### ✅ Passing Gates

1. **Test-Driven Development (Principle II)**: ✅ PASS
   - Plan includes comprehensive pytest-based testing
   - TDD workflow applies to Python implementation
   - Integration tests with real C++ code samples

2. **Zero-Defect Commitment (Principle I)**: ✅ PASS
   - All tests must pass
   - Python linting (ruff/pylint) replaces C++ static analysis
   - Type checking with mypy
   - 100% accuracy requirement per SC-002

3. **Dependency Hygiene (Principle VII)**: ⚠️ NEEDS RESEARCH
   - Must select actively maintained C++ parser library
   - Lock versions in pyproject.toml (uv manages this)
   - Justify parser choice in research phase

4. **Build Verification (Principle VI)**: ✅ PASS (adapted for Python)
   - Zero warnings from linters (ruff, mypy)
   - CI pipeline with automated tests
   - Cross-platform validation (Linux, macOS, Windows)

### ⚠️ Principles Requiring Adaptation

1. **Code Quality Standards (Principle III)**: Adapted for Python
   - Modern Python (3.11+) instead of C++17
   - Type hints (mypy) for type safety
   - Clear naming, PEP 8 compliance
   - Maximum function complexity ≤10 (same as C++)

2. **Static Analysis First (Principle IV)**: Adapted for Python
   - ruff (linter) instead of clang-tidy
   - mypy (type checker) instead of C++ compiler checks
   - No sanitizers (Python memory-managed)
   - Security: bandit for Python security issues

3. **Memory Safety (Principle V)**: Adapted for Python
   - Python garbage collection handles most memory
   - Must monitor memory usage to stay <2GB (SC-001a)
   - Use memory_profiler during testing
   - Handle large files efficiently (streaming/chunking if needed)

### ❌ Not Applicable

- C++ specific tools (clang-tidy, cppcheck, ASan, UBSan, TSan, Valgrind)
- C++ RAII patterns (Python uses context managers)
- CMake (using uv for Python project management)

### Constitution Compliance Summary

**Status**: ✅ COMPLIANT with adaptations

The project follows the spirit of the constitution (zero-defect, TDD, quality standards, dependency hygiene) adapted for Python tooling. The Python implementation will analyze C++ code but is not itself subject to C++ quality gates.

## Project Structure

### Documentation (this feature)

```text
specs/001-function-grouper/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)

```text
cpp-dependency-analysis/
├── pyproject.toml           # uv project configuration
├── uv.lock                  # Locked dependencies
├── README.md
├── .python-version          # Python version specification
├── src/
│   └── function_grouper/
│       ├── __init__.py
│       ├── __main__.py      # CLI entry point
│       ├── cli/
│       │   ├── __init__.py
│       │   ├── main.py      # Command-line interface (argparse/click)
│       │   └── progress.py  # Progress indication
│       ├── parser/
│       │   ├── __init__.py
│       │   ├── cpp_parser.py       # C++ AST parsing
│       │   └── function_extractor.py # Extract function definitions
│       ├── analyzer/
│       │   ├── __init__.py
│       │   ├── dependency_graph.py # Graph construction
│       │   ├── call_analyzer.py    # Identify function calls
│       │   └── grouper.py          # Find independent groups (connected components)
│       ├── formatter/
│       │   ├── __init__.py
│       │   ├── json_formatter.py   # JSON output
│       │   ├── text_formatter.py   # Human-readable text
│       │   └── dot_formatter.py    # Graphviz DOT format
│       └── models/
│           ├── __init__.py
│           ├── function.py         # Function dataclass
│           ├── call_graph.py       # Call graph dataclass
│           └── group.py            # Function group dataclass
├── tests/
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   ├── contract/
│   │   ├── __init__.py
│   │   ├── test_cli_interface.py    # CLI contract tests
│   │   └── test_output_formats.py   # JSON/text/DOT format contracts
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_end_to_end.py       # Full workflow tests
│   │   ├── test_large_files.py      # Performance/scalability tests
│   │   └── fixtures/                # Sample C++ files
│   │       ├── simple_independent.cpp
│   │       ├── complex_dependencies.cpp
│   │       ├── circular_deps.cpp
│   │       └── large_10k_lines.cpp
│   └── unit/
│       ├── __init__.py
│       ├── test_parser.py
│       ├── test_analyzer.py
│       ├── test_grouper.py
│       └── test_formatters.py
└── .github/
    └── workflows/
        └── ci.yml                   # CI pipeline (pytest, linting, type-checking)
```

**Structure Decision**: Single Python CLI application following modern Python project layout. Using `src/` layout for better isolation and testing. The `function_grouper` package contains modular components:
- **cli/**: User interface and progress reporting
- **parser/**: C++ AST parsing (library TBD in research phase)
- **analyzer/**: Dependency graph construction and grouping logic
- **formatter/**: Multiple output format support
- **models/**: Data classes for Function, CallGraph, Group

Tests are organized by type (contract, integration, unit) per constitution testing standards. Integration tests include C++ fixture files for realistic testing.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations detected. The Python-specific adaptations are reasonable translations of C++ principles to Python tooling and do not violate the spirit of the constitution.
