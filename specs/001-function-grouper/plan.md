# Implementation Plan: C++ Function Grouper

**Branch**: `001-function-grouper` | **Date**: 2025-10-27 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-function-grouper/spec.md`

## Summary

Build a command-line tool that analyzes C++ source files to identify independent function groups based on call relationships. The tool parses C++ files using libclang to build an Abstract Syntax Tree (AST), constructs a directed call graph, and uses connected component analysis to identify groups of functions that do not reference each other. Output formats include JSON (structured data), plain text (human-readable), and DOT (Graphviz visualization).

**Technical Approach**: Python 3.11+ with libclang 18.1.1+ for C++ AST parsing, networkx for graph algorithms, and click for CLI framework.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: libclang 18.1.1+ (C++ AST parser with full C++17/C++20 support), click (CLI framework), networkx (graph algorithms)
**Storage**: N/A (processes files in-memory, outputs to stdout or specified file)
**Testing**: pytest (unit/integration/contract tests), pytest-cov (coverage), mypy (type checking), ruff (linting)
**Target Platform**: Linux, macOS (cross-platform via libclang binary wheels)
**Project Type**: single (CLI tool with library components)
**Performance Goals**: Parse 10,000-line files in under 30 seconds, handle up to 1000 function definitions
**Constraints**: <2GB memory usage, 95%+ parse success rate on real-world C++ code
**Scale/Scope**: Single-file analysis, modern C++ (C++17 baseline, C++20 support)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Zero-Defect Commitment ✅
- **Status**: PASS
- **Evidence**: All quality gates defined in tasks.md (tests, sanitizers not applicable to Python, linting via ruff)
- **Action**: No violations

### II. Test-Driven Development (NON-NEGOTIABLE) ✅
- **Status**: PASS
- **Evidence**: Test tasks precede implementation tasks in tasks.md, TDD workflow enforced
- **Action**: No violations

### III. Code Quality Standards ✅
- **Status**: PASS (adapted for Python)
- **Evidence**: Using modern Python 3.11+, type hints enforced via mypy, ruff for linting, maximum function complexity enforced
- **Action**: No violations (C++-specific standards not applicable)

### IV. Static Analysis First ✅
- **Status**: PASS (adapted for Python)
- **Evidence**: Using ruff (linter), mypy (type checker) before code review
- **Action**: No violations (C++ sanitizers not applicable, using Python equivalents)

### V. Memory Safety ✅
- **Status**: PASS (adapted for Python)
- **Evidence**: Python provides automatic memory management, performance tests include memory usage limits (<2GB)
- **Action**: No violations (Python handles memory safety, no manual allocation)

### VI. Build Verification ✅
- **Status**: PASS
- **Evidence**: All tests must pass before commit, dependency versions locked in pyproject.toml, cross-platform validation (Linux, macOS)
- **Action**: No violations

### VII. Dependency Hygiene ✅
- **Status**: PASS
- **Evidence**: Minimal dependencies (libclang, click, networkx), all actively maintained, versions locked, justifications documented in research.md
- **Action**: No violations

### VIII. Comprehensive Documentation ⚠️ REQUIRES ATTENTION
- **Status**: PASS (with action items)
- **Evidence**: README.md exists with installation, usage, examples
- **Action Required**:
  - Verify all README.md code samples are runnable
  - Add comprehensive examples covering all output formats (JSON, text, DOT)
  - Include troubleshooting section for common issues
  - Add sample verification step to tasks.md

### IX. Sample-Driven Verification ⚠️ REQUIRES ATTENTION
- **Status**: REQUIRES IMPLEMENTATION
- **Evidence**: Not yet implemented in workflow
- **Action Required**:
  - Add sample generation tasks to tasks.md for each user story
  - Generate real C++ sample files demonstrating tool functionality
  - Add verification tasks to execute samples and validate output
  - Include samples in integration tests or examples/ directory

**Constitution Compliance**: 7/9 principles fully compliant, 2/9 require additional implementation (Principles VIII and IX - documentation and sample verification)

**Post-Design Re-Check**: After Phase 1 completion, verify that:
1. README.md includes verified runnable samples for all output formats
2. Sample verification tasks are added to implementation workflow
3. All code examples in documentation are tested

## Project Structure

### Documentation (this feature)

```text
specs/001-function-grouper/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output - C++ parser library comparison (COMPLETE)
├── data-model.md        # Phase 1 output - Data structures and entities (COMPLETE)
├── quickstart.md        # Phase 1 output - Developer quickstart guide (COMPLETE)
├── contracts/           # Phase 1 output - CLI interface contracts (COMPLETE)
│   ├── cli-interface.md
│   └── output-formats.md
└── tasks.md             # Phase 2 output (/speckit.tasks command) (COMPLETE)
```

### Source Code (repository root)

```text
cpp-dependency-analysis/
├── src/function_grouper/       # Main package
│   ├── __init__.py
│   ├── parser/                 # C++ AST parsing module
│   │   ├── __init__.py
│   │   ├── clang_parser.py     # libclang wrapper for C++ parsing
│   │   ├── function_extractor.py # Extract function definitions and calls
│   │   └── ast_visitor.py      # AST traversal utilities
│   ├── analyzer/               # Call graph and grouping logic
│   │   ├── __init__.py
│   │   ├── call_graph.py       # Build directed call graph
│   │   ├── group_detector.py   # Connected component analysis
│   │   └── dependency_analyzer.py # Identify dependencies
│   ├── formatter/              # Output formatting
│   │   ├── __init__.py
│   │   ├── json_formatter.py   # JSON output
│   │   ├── text_formatter.py   # Human-readable text
│   │   └── dot_formatter.py    # Graphviz DOT format
│   ├── cli/                    # Command-line interface
│   │   ├── __init__.py
│   │   └── main.py             # Click CLI entry point
│   └── models/                 # Data models
│       ├── __init__.py
│       ├── function.py         # Function entity
│       ├── call_graph.py       # CallGraph entity
│       └── function_group.py   # FunctionGroup entity
│
├── tests/                      # Test suite
│   ├── contract/               # CLI contract tests
│   │   ├── test_cli_interface.py
│   │   └── test_output_formats.py
│   ├── integration/            # Integration tests
│   │   ├── test_end_to_end.py
│   │   └── test_real_world_files.py
│   └── unit/                   # Unit tests
│       ├── test_parser.py
│       ├── test_analyzer.py
│       ├── test_formatter.py
│       └── test_models.py
│
├── examples/                   # Sample C++ files and outputs (NEW - for Principle IX)
│   ├── simple.cpp              # Simple example with 3 independent functions
│   ├── simple_output.json      # Expected JSON output
│   ├── simple_output.txt       # Expected text output
│   ├── complex.cpp             # Complex example with circular dependencies
│   └── README.md               # Guide to examples
│
├── pyproject.toml              # Python project configuration
├── README.md                   # User documentation (updated per Principle VIII)
├── CONTRIBUTING.md             # Contributor guidelines
└── LICENSE
```

**Structure Decision**: Single project structure selected because this is a CLI tool with library components. No frontend/backend separation needed. The project uses Python's standard package layout with clear separation of concerns: parser (AST analysis), analyzer (graph algorithms), formatter (output generation), and cli (user interface).

## Compliance with New Constitution Principles

### Principle VIII: Comprehensive Documentation

**Current Status**: README.md exists but requires verification

**Required Actions**:
1. **Verify Runnable Samples**: All code examples in README.md must be executable
2. **Add Comprehensive Examples**:
   - Installation example (pip install)
   - Basic usage (analyze simple C++ file)
   - Advanced usage (all output formats: JSON, text, DOT)
   - Include paths example
   - Error handling example
3. **Maintain Documentation**: Update README.md whenever features change
4. **Troubleshooting Section**: Add common issues and solutions

**Implementation Timeline**: Include in Phase 3 (Polish & Documentation)

### Principle IX: Sample-Driven Verification

**Current Status**: Not yet implemented

**Required Actions**:
1. **Create examples/ Directory**: Add sample C++ files demonstrating tool functionality
2. **Generate Sample Files**:
   - `examples/simple.cpp`: 3-5 functions, 2 independent groups
   - `examples/complex.cpp`: 10+ functions, circular dependencies, templates
   - `examples/edge_cases.cpp`: Recursion, overloads, lambdas
3. **Execute Samples**: Run tool against each sample file
4. **Verify Output**: Validate that output matches expected results
5. **Include in Tests**: Integration tests should use sample files
6. **Document Samples**: `examples/README.md` explaining each sample

**Implementation Timeline**: Include in Phase 3 (Polish & Documentation), before marking tasks complete

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations requiring justification. All constitution principles are either fully compliant or have clear action items for compliance (Principles VIII and IX require additional documentation and sample verification work, which is planned).

## Phase 0: Research (COMPLETE)

**Status**: ✅ COMPLETE

**Artifacts**: [research.md](research.md)

**Key Decisions**:
- **Parser Library**: libclang 18.1.1+ selected over tree-sitter, pycparser, cxxheaderparser
- **Rationale**: Full C++17/C++20 support, semantic analysis capabilities, active maintenance
- **Graph Library**: networkx for connected component analysis
- **CLI Framework**: click for command-line interface

## Phase 1: Design & Contracts (COMPLETE)

**Status**: ✅ COMPLETE

**Artifacts**:
- [data-model.md](data-model.md) - Data structures (Function, CallGraph, FunctionGroup)
- [contracts/cli-interface.md](contracts/cli-interface.md) - Command-line interface specification
- [contracts/output-formats.md](contracts/output-formats.md) - JSON, text, DOT output schemas
- [quickstart.md](quickstart.md) - Developer setup and quickstart guide

**Key Designs**:
- **Data Model**: Function, SourceLocation, FunctionKind, ParseStatus, CallGraph, FunctionGroup entities
- **CLI Interface**: `function-grouper [OPTIONS] FILE` with `-f/--format`, `-o/--output`, `-I/--include-path` flags
- **Output Formats**: JSON (machine-readable), text (human-readable), DOT (visualization)

## Phase 2: Implementation (READY TO START)

**Status**: ⚠️ READY - tasks.md exists, awaiting execution via `/speckit.implement`

**Next Steps**: Run `/speckit.implement` to execute tasks in tasks.md

**Constitution Compliance Notes**:
1. Before marking tasks complete, ensure Principle IX (Sample-Driven Verification) is satisfied:
   - Generate sample C++ files
   - Execute tool against samples
   - Verify output correctness
2. Update README.md to satisfy Principle VIII (Comprehensive Documentation):
   - Add verified runnable examples
   - Include troubleshooting section
   - Document all features and use cases

## Summary

This implementation plan is ready for Phase 2 execution. All design artifacts (research, data model, contracts, quickstart) are complete. The plan now includes explicit requirements for:

1. **Documentation Quality (Principle VIII)**: README.md must contain verified runnable samples covering all features
2. **Sample Verification (Principle IX)**: Before task completion, generate and execute representative samples

These additions ensure compliance with the updated constitution v1.1.0 and improve the quality and usability of the delivered tool.

**Branch**: `001-function-grouper`
**Implementation Plan**: `/Users/yinghanhung/Projects/AI/cpp-dependency-analysis/specs/001-function-grouper/plan.md`
**Generated Artifacts**: research.md, data-model.md, contracts/, quickstart.md, tasks.md (all complete)
**Next Command**: `/speckit.implement` to execute implementation tasks
