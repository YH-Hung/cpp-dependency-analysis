<!--
SYNC IMPACT REPORT
==================
Version Change: 1.0.0 → 1.1.0 (Added Documentation & Verification Principles)
Constitution Type: MINOR (Added 2 new principles expanding governance)

Principles Modified:
- VIII. Comprehensive Documentation (NEW - added README maintenance requirement)
- IX. Sample-Driven Verification (NEW - added sample generation and verification requirement)

Added Sections:
- Principle VIII: Comprehensive Documentation
- Principle IX: Sample-Driven Verification

Removed Sections: None

Template Sync Status:
✅ plan-template.md - Constitution Check section references this file
✅ spec-template.md - Aligned with testing/quality requirements
✅ tasks-template.md - Task categorization reflects principle-driven types (should include documentation and sample verification tasks)
⚠️  README.md - Should be reviewed to ensure it meets new Principle VIII standards
⚠️  Implementation workflows - Should incorporate Principle IX sample verification before task completion

Follow-up TODOs:
- Review README.md for compliance with Principle VIII (comprehensive, runnable samples)
- Update implementation workflow to include sample generation and verification step (Principle IX)
- Consider adding documentation quality checks to CI/CD pipeline
-->

# C++ Dependency Analysis Tool Constitution

## Core Principles

### I. Zero-Defect Commitment

Every release MUST be bug-free. Code is only considered complete when it passes ALL quality gates:
- All tests passing (unit, integration, contract)
- Zero compiler warnings on strictest settings (-Wall -Wextra -Werror)
- Zero static analysis violations
- Zero memory leaks or undefined behavior detected by sanitizers
- All edge cases documented and tested

**Rationale**: A dependency analysis tool must be trustworthy. Users rely on accurate dependency graphs; any bug could lead to incorrect build decisions, security vulnerabilities, or broken deployments.

### II. Test-Driven Development (NON-NEGOTIABLE)

TDD is mandatory for ALL features:
1. Write failing tests FIRST (unit + integration)
2. Obtain approval/review of test coverage
3. Verify tests fail for the right reasons
4. Implement minimum code to pass tests
5. Refactor while keeping tests green
6. Add edge case tests before marking complete

**Rationale**: C++ code is complex and error-prone. Writing tests first ensures we build exactly what's needed and can refactor confidently. Red-Green-Refactor cycle prevents over-engineering.

### III. Code Quality Standards

All code MUST meet these non-negotiable standards:
- Modern C++ (C++17 minimum, C++20 preferred)
- RAII for all resource management (no manual new/delete)
- Const-correctness enforced everywhere
- No raw pointers except for non-owning references
- Smart pointers (unique_ptr, shared_ptr) for ownership
- Comprehensive error handling (no silent failures)
- Self-documenting code: clear names, minimal comments except for "why"
- Maximum function complexity: cyclomatic complexity ≤ 10

**Rationale**: High-quality C++ code prevents bugs at compile time. Following modern idioms reduces memory errors, resource leaks, and undefined behavior.

### IV. Static Analysis First

Before ANY code review or commit:
- clang-tidy MUST pass with project .clang-tidy config
- cppcheck MUST report zero issues
- Address Sanitizer (ASan) MUST pass on test suite
- Undefined Behavior Sanitizer (UBSan) MUST pass
- Thread Sanitizer (TSan) for concurrent code

**Rationale**: Static analysis catches bugs humans miss. Running sanitizers during tests catches memory errors, data races, and undefined behavior before they reach production.

### V. Memory Safety

All code MUST be memory-safe:
- Valgrind clean (zero leaks, zero invalid access)
- No use-after-free, double-free, or buffer overflows
- All heap allocations tracked and freed
- RAII wrappers for all external resources (files, sockets, etc.)
- Bounds checking for array/vector access
- Safe string handling (no C-style char* manipulation)

**Rationale**: Memory bugs are the #1 source of crashes and security vulnerabilities in C++. A dependency analysis tool must process large codebases reliably without crashes or memory exhaustion.

### VI. Build Verification

Continuous verification at every stage:
- Code MUST build with zero warnings (-Wall -Wextra -Werror)
- All tests MUST pass before commit
- CMake configuration MUST be warning-free
- Cross-platform builds validated (Linux, macOS minimum)
- Build time monitored (no regressions >10% without justification)
- Dependencies MUST specify exact versions (no "latest")

**Rationale**: Clean builds prevent hidden issues. Cross-platform validation ensures portability. Build time matters for developer productivity.

### VII. Dependency Hygiene

Dependency management rules:
- Minimize external dependencies (justify each addition)
- Prefer header-only libraries where appropriate
- All dependencies MUST be actively maintained
- Security vulnerabilities in dependencies = BLOCKER
- Lock dependency versions in CMakeLists.txt
- Document why each dependency is needed
- Provide fallback/mock for testing without external deps

**Rationale**: Dependency analysis tools should model good dependency hygiene. Fewer dependencies = fewer security risks, easier builds, more reliable software.

### VIII. Comprehensive Documentation

README.md and user-facing documentation MUST be:
- Comprehensive: Cover all features and use cases
- Maintained: Updated with every feature change
- Runnable: Include fully executable code samples
- Verified: All code samples MUST be tested and working
- Complete: Include installation, usage, examples, and troubleshooting
- Accessible: Clear for both beginners and advanced users

**Rationale**: Documentation is the first touchpoint for users. Poor or outdated documentation undermines user trust and adoption. Runnable samples ensure documentation stays synchronized with code and provides immediate value to users evaluating or learning the tool.

### IX. Sample-Driven Verification

Before marking any task complete:
- MUST generate representative code samples demonstrating the feature
- MUST actually execute samples against the implementation
- MUST verify samples produce expected results
- MUST include samples in documentation or test suite
- Samples MUST cover typical use cases, not just happy paths
- Failed sample execution = incomplete implementation

**Rationale**: Sample verification bridges the gap between passing tests and real-world usability. A feature that passes unit tests but fails with realistic examples is not production-ready. Generating and running samples catches integration issues, usability problems, and documentation gaps before release.

## Testing Standards

### Test Categories

1. **Unit Tests**:
   - Test individual classes/functions in isolation
   - Fast (<1ms per test)
   - 100% code coverage for critical paths
   - Mock external dependencies

2. **Integration Tests**:
   - Test component interactions
   - Real file system, real dependency graphs
   - Performance benchmarks included
   - Test with realistic C++ projects

3. **Contract Tests**:
   - CLI interface contracts (input/output formats)
   - API contracts if library mode exists
   - Backward compatibility guarantees

### Test Requirements

- ALL tests automated (no manual testing except exploratory)
- Tests MUST be deterministic (no flaky tests)
- Tests MUST be isolated (order-independent)
- Performance regression tests for critical operations
- Test data includes real-world C++ projects (small/medium/large)

## Code Review Requirements

Before merge, code MUST:
1. Pass all automated checks (CI pipeline)
2. Have peer review approval
3. Include test coverage report
4. Update documentation if behavior changed
5. Pass constitution compliance check

## Development Workflow

### Feature Development Flow

1. **Specification Phase**:
   - Write user stories with acceptance criteria
   - Identify affected components
   - Plan test strategy

2. **TDD Phase**:
   - Write failing tests
   - Get test review
   - Implement to pass tests
   - Refactor

3. **Quality Gate Phase**:
   - Static analysis clean
   - Memory checks clean
   - Performance benchmarks pass
   - Documentation updated

4. **Review Phase**:
   - Code review
   - Constitution compliance check
   - Integration testing
   - Merge

### Bug Fix Flow

1. Write failing test reproducing bug
2. Fix bug (minimum change)
3. Verify test passes
4. Add regression test if needed
5. Full quality gate check
6. Review and merge

## Governance

### Amendment Process

1. Propose amendment with rationale
2. Impact analysis on existing code/practices
3. Team discussion and approval
4. Update constitution version (semantic versioning)
5. Update dependent templates
6. Communicate to all contributors

### Version Semantics

- **MAJOR**: Removes/redefines principles, breaking changes to standards
- **MINOR**: Adds new principles or expands existing ones
- **PATCH**: Clarifications, typo fixes, non-semantic updates

### Compliance

- All PRs MUST verify compliance with constitution
- Violations require explicit justification (documented in complexity tracking)
- Constitution supersedes all other development practices
- Quarterly constitution review to ensure it serves project needs

### Living Document

This constitution evolves with the project. When principles become outdated or overly burdensome, propose amendments. But changes require careful consideration and team consensus.

**Version**: 1.1.0 | **Ratified**: 2025-10-25 | **Last Amended**: 2025-10-27
