# Tasks: C++ Function Grouper

**Input**: Design documents from `/specs/001-function-grouper/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/, quickstart.md

**Tests**: Tests are included per the constitution requirement (TDD approach with pytest)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Updated**: 2025-10-27 - Added Phases 9 & 10 for Constitution v1.1.0 compliance (Principles VIII & IX)
- **Phase 9**: Sample Generation & Verification (Principle IX - sample-driven verification)
- **Phase 10**: Comprehensive Documentation (Principle VIII - comprehensive documentation with runnable samples)
- **Total**: 223 tasks (was 175, added 48 for constitution compliance)

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/function_grouper/`, `tests/` at repository root
- Paths follow the structure defined in plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project directory structure (src/function_grouper/, tests/, .github/workflows/)
- [ ] T002 Initialize uv project with pyproject.toml configuration for Python 3.11+
- [ ] T003 Add core dependencies to pyproject.toml: libclang>=18.1.1, click>=8.1.0, networkx>=3.0
- [ ] T004 [P] Add dev dependencies to pyproject.toml: pytest, pytest-cov, pytest-benchmark, mypy, ruff, memory-profiler
- [ ] T005 [P] Create .python-version file specifying Python 3.11
- [ ] T006 [P] Configure ruff linting settings in pyproject.toml (line-length=100, target-version=py311)
- [ ] T007 [P] Configure mypy type checking in pyproject.toml (strict mode, Python 3.11)
- [ ] T008 [P] Configure pytest settings in pyproject.toml (testpaths, coverage options)
- [ ] T009 [P] Create src/function_grouper/__init__.py
- [ ] T010 [P] Create tests/__init__.py and tests/conftest.py for pytest fixtures

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data models and infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T011 [P] Create FunctionKind enum in src/function_grouper/models/function.py
- [ ] T012 [P] Create ParseStatus enum in src/function_grouper/models/function.py
- [ ] T013 Create SourceLocation dataclass in src/function_grouper/models/function.py
- [ ] T014 Create Function dataclass in src/function_grouper/models/function.py with all attributes from data-model.md
- [ ] T015 [P] Create CallEdge dataclass in src/function_grouper/models/call_graph.py
- [ ] T016 Create CallGraph class in src/function_grouper/models/call_graph.py with graph manipulation methods
- [ ] T017 [P] Create FunctionGroup dataclass in src/function_grouper/models/group.py
- [ ] T018 [P] Create GraphMetadata dataclass in src/function_grouper/models/call_graph.py
- [ ] T019 [P] Create src/function_grouper/models/__init__.py exporting all model classes
- [ ] T020 [P] Create test fixtures directory tests/integration/fixtures/
- [ ] T021 [P] Create simple_independent.cpp test fixture in tests/integration/fixtures/
- [ ] T022 [P] Create complex_dependencies.cpp test fixture in tests/integration/fixtures/
- [ ] T023 [P] Create circular_deps.cpp test fixture in tests/integration/fixtures/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Analyze Function Independence (Priority: P1) 🎯 MVP

**Goal**: Parse C++ files, identify function definitions and calls, group functions by independence

**Independent Test**: Provide a C++ file with known function dependencies and verify the tool correctly identifies all independent groups. Can test with simple_independent.cpp (expect 3 groups) and complex_dependencies.cpp (expect 2 groups).

### Tests for User Story 1 - Write FIRST, ensure they FAIL before implementation

- [ ] T024 [P] [US1] Unit test for CppParser.parse_file() with simple function in tests/unit/test_parser.py
- [ ] T025 [P] [US1] Unit test for CppParser extracting function names and signatures in tests/unit/test_parser.py
- [ ] T026 [P] [US1] Unit test for CppParser identifying function calls in tests/unit/test_parser.py
- [ ] T027 [P] [US1] Unit test for CallGraph.add_function() in tests/unit/test_analyzer.py
- [ ] T028 [P] [US1] Unit test for CallGraph.add_call() in tests/unit/test_analyzer.py
- [ ] T029 [P] [US1] Unit test for Grouper.find_connected_components() in tests/unit/test_grouper.py
- [ ] T030 [P] [US1] Integration test for end-to-end analysis with simple_independent.cpp in tests/integration/test_end_to_end.py
- [ ] T031 [P] [US1] Integration test for end-to-end analysis with complex_dependencies.cpp in tests/integration/test_end_to_end.py

### Implementation for User Story 1

- [ ] T032 [P] [US1] Create CppParser class skeleton in src/function_grouper/parser/cpp_parser.py
- [ ] T033 [P] [US1] Create FunctionExtractor helper class in src/function_grouper/parser/function_extractor.py
- [ ] T034 [US1] Implement CppParser.__init__() with libclang Index creation
- [ ] T035 [US1] Implement CppParser.parse_file() to create translation unit with args from CLI
- [ ] T036 [US1] Implement FunctionExtractor.extract_functions() to traverse AST and find FUNCTION_DECL nodes
- [ ] T037 [US1] Implement FunctionExtractor._determine_function_kind() to classify function types (free, member, static, etc.)
- [ ] T038 [US1] Implement FunctionExtractor._extract_calls() to find CALL_EXPR nodes within function bodies
- [ ] T039 [US1] Implement FunctionExtractor._build_qualified_name() to handle namespaces and classes
- [ ] T040 [US1] Add error handling for parse failures in CppParser (graceful degradation per FR-014)
- [ ] T041 [P] [US1] Create src/function_grouper/parser/__init__.py exporting CppParser
- [ ] T042 [P] [US1] Create CallAnalyzer class in src/function_grouper/analyzer/call_analyzer.py
- [ ] T043 [US1] Implement CallAnalyzer.build_call_graph() to convert Function list to CallGraph
- [ ] T044 [US1] Implement CallGraph.get_callers() method
- [ ] T045 [US1] Implement CallGraph.get_callees() method
- [ ] T046 [US1] Implement CallGraph.has_cycle() using networkx cycle detection
- [ ] T047 [US1] Implement CallGraph.find_cycles() using networkx algorithms
- [ ] T048 [P] [US1] Create Grouper class in src/function_grouper/analyzer/grouper.py
- [ ] T049 [US1] Implement Grouper.find_independent_groups() using networkx.connected_components()
- [ ] T050 [US1] Implement Grouper._compute_group_statistics() to populate internal_edges, external_edges, has_cycles
- [ ] T051 [US1] Implement Grouper._check_independence() to determine is_independent flag
- [ ] T052 [P] [US1] Create src/function_grouper/analyzer/__init__.py exporting analyzer classes
- [ ] T053 [US1] Add validation in CallGraph to ensure all edges reference existing functions
- [ ] T054 [US1] Add validation to handle function overloading correctly (FR-006)
- [ ] T055 [US1] Add handling for recursive functions (FR-011)
- [ ] T056 [US1] Add handling for template functions (FR-007)
- [ ] T057 [US1] Add handling for member functions and free functions (FR-009)

**Checkpoint**: At this point, User Story 1 core functionality (parsing, analyzing, grouping) should be fully functional and testable independently

---

## Phase 4: User Story 2 - Visualize Function Relationships (Priority: P2)

**Goal**: Provide clear output showing function call relationships and group structure in multiple formats

**Independent Test**: Run tool on complex_dependencies.cpp and verify output clearly shows which functions call which, and groups are labeled correctly. Test JSON schema compliance, text readability, and DOT validity.

### Tests for User Story 2 - Write FIRST, ensure they FAIL

- [ ] T058 [P] [US2] Unit test for JSONFormatter.format() in tests/unit/test_formatters.py
- [ ] T059 [P] [US2] Unit test for TextFormatter.format() in tests/unit/test_formatters.py
- [ ] T060 [P] [US2] Unit test for DOTFormatter.format() in tests/unit/test_formatters.py
- [ ] T061 [P] [US2] Contract test for JSON output schema compliance in tests/contract/test_output_formats.py
- [ ] T062 [P] [US2] Contract test for DOT format validity (parseable by Graphviz) in tests/contract/test_output_formats.py
- [ ] T063 [P] [US2] Integration test for circular dependency detection and reporting in tests/integration/test_end_to_end.py

### Implementation for User Story 2

- [ ] T064 [P] [US2] Create JSONFormatter class in src/function_grouper/formatter/json_formatter.py
- [ ] T065 [P] [US2] Create TextFormatter class in src/function_grouper/formatter/text_formatter.py
- [ ] T066 [P] [US2] Create DOTFormatter class in src/function_grouper/formatter/dot_formatter.py
- [ ] T067 [US2] Implement JSONFormatter.format() to output JSON per schema in contracts/json-output-schema.json
- [ ] T068 [US2] Implement JSONFormatter._format_metadata() to create metadata section
- [ ] T069 [US2] Implement JSONFormatter._format_functions() to create functions array
- [ ] T070 [US2] Implement JSONFormatter._format_groups() to create groups array
- [ ] T071 [US2] Implement JSONFormatter._format_parse_errors() to create parse_errors array
- [ ] T072 [US2] Implement TextFormatter.format() to create human-readable output per contracts/cli-interface.md
- [ ] T073 [US2] Implement TextFormatter._format_summary() to create summary section
- [ ] T074 [US2] Implement TextFormatter._format_groups() to create groups section with dependency info
- [ ] T075 [US2] Implement TextFormatter._format_parse_errors() to list errors
- [ ] T076 [US2] Implement DOTFormatter.format() to create Graphviz DOT output
- [ ] T077 [US2] Implement DOTFormatter._create_nodes() to define function nodes
- [ ] T078 [US2] Implement DOTFormatter._create_edges() to define call relationships
- [ ] T079 [US2] Implement DOTFormatter._create_subgraphs() to visualize groups with cluster subgraphs
- [ ] T080 [US2] Add circular dependency highlighting in DOTFormatter (different color/style)
- [ ] T081 [P] [US2] Create src/function_grouper/formatter/__init__.py exporting all formatters
- [ ] T082 [US2] Add JSON schema validation against contracts/json-output-schema.json
- [ ] T083 [US2] Ensure all output is UTF-8 encoded

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - can analyze and visualize in all 3 formats

---

## Phase 5: User Story 3 - Export Grouped Functions (Priority: P3)

**Goal**: Provide export suggestions showing how to split the file based on independent groups

**Independent Test**: Analyze a file with multiple groups, request export suggestions, verify suggestions include file names, function lists, and required headers for each group.

### Tests for User Story 3 - Write FIRST, ensure they FAIL

- [ ] T084 [P] [US3] Unit test for ExportSuggester.suggest_file_splits() in tests/unit/test_export.py
- [ ] T085 [P] [US3] Unit test for ExportSuggester._identify_required_headers() in tests/unit/test_export.py
- [ ] T086 [P] [US3] Integration test for export suggestions with real C++ file in tests/integration/test_export_suggestions.py

### Implementation for User Story 3

- [ ] T087 [US3] Create ExportSuggester class in src/function_grouper/analyzer/export_suggester.py
- [ ] T088 [US3] Implement ExportSuggester.suggest_file_splits() to generate split recommendations
- [ ] T089 [US3] Implement ExportSuggester._generate_filename_suggestions() based on group functions
- [ ] T090 [US3] Implement ExportSuggester._identify_required_headers() by analyzing includes used by group
- [ ] T091 [US3] Implement ExportSuggester._detect_imbalanced_groups() to warn about large groups
- [ ] T092 [US3] Add export suggestions to JSON output format
- [ ] T093 [US3] Add export suggestions to text output format
- [ ] T094 [US3] Add CLI flag --export-suggestions to enable this feature

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: CLI Integration

**Purpose**: Complete command-line interface per contracts/cli-interface.md

### Tests for CLI - Write FIRST, ensure they FAIL

- [ ] T095 [P] Contract test for CLI help output in tests/contract/test_cli_interface.py
- [ ] T096 [P] Contract test for CLI version output in tests/contract/test_cli_interface.py
- [ ] T097 [P] Contract test for CLI argument validation in tests/contract/test_cli_interface.py
- [ ] T098 [P] Contract test for CLI exit codes in tests/contract/test_cli_interface.py
- [ ] T099 [P] Contract test for CLI format flag (-f json/text/dot) in tests/contract/test_cli_interface.py
- [ ] T100 [P] Contract test for CLI output flag (-o file) in tests/contract/test_cli_interface.py
- [ ] T101 [P] Integration test for CLI with all three output formats in tests/integration/test_cli_integration.py

### Implementation for CLI

- [ ] T102 Create Click application skeleton in src/function_grouper/cli/main.py
- [ ] T103 Add required argument <input-file> with validation (exists, readable, <100MB)
- [ ] T104 [P] Add option -f/--format with choices (json, text, dot) and default text
- [ ] T105 [P] Add option -o/--output for output file with overwrite confirmation
- [ ] T106 [P] Add option --std with C++ version choices (c++11/14/17/20/23) and default c++17
- [ ] T107 [P] Add option -I/--include for include paths (repeatable)
- [ ] T108 [P] Add option --progress/--no-progress flag with default enabled
- [ ] T109 [P] Add option -v/--verbose (count flag for verbosity levels)
- [ ] T110 [P] Add option -q/--quiet (mutually exclusive with verbose)
- [ ] T111 [P] Add option --strict/--no-strict for error handling mode
- [ ] T112 [P] Add option -h/--help (Click provides automatically)
- [ ] T113 [P] Add option --version showing tool version, libclang version, Python version
- [ ] T114 [P] Add option --force to skip overwrite confirmation
- [ ] T115 [P] Add option --export-suggestions for US3 feature
- [ ] T116 Implement main() function orchestrating: parse → analyze → group → format → output
- [ ] T117 Add error handling for all exit codes per contracts/cli-interface.md (codes 0-8)
- [ ] T118 Implement output to stdout or file based on -o flag
- [ ] T119 Add validation that -q and -v are mutually exclusive
- [ ] T120 Create entry point in src/function_grouper/__main__.py calling cli.main.main()
- [ ] T121 Configure project.scripts in pyproject.toml: function-grouper = function_grouper.cli.main:main

---

## Phase 7: Progress Indication & Error Handling

**Purpose**: User experience improvements for long-running operations

### Tests - Write FIRST

- [ ] T122 [P] Unit test for ProgressReporter.update() in tests/unit/test_progress.py
- [ ] T123 [P] Integration test for progress output format in tests/integration/test_progress.py

### Implementation

- [ ] T124 Create ProgressReporter class in src/function_grouper/cli/progress.py
- [ ] T125 Implement ProgressReporter.start() to initialize progress bar to stderr
- [ ] T126 Implement ProgressReporter.update(percentage, phase) following contracts/cli-interface.md format
- [ ] T127 Implement ProgressReporter.finish() to complete progress bar
- [ ] T128 Integrate progress reporting into CppParser for parsing phase
- [ ] T129 Integrate progress reporting into CallAnalyzer for graph building phase
- [ ] T130 Integrate progress reporting into Grouper for grouping phase
- [ ] T131 Integrate progress reporting into formatters for output phase
- [ ] T132 Add graceful error handling for parse errors (FR-014) - continue with partial analysis
- [ ] T133 Add detailed error messages per contracts/cli-interface.md format (type, description, context, suggestion)
- [ ] T134 Add memory usage tracking to GraphMetadata using memory_profiler
- [ ] T135 Add timeout handling to prevent indefinite hangs
- [ ] T136 Add error exit with code 7 if memory exceeds 2GB limit (SC-001a)

---

## Phase 8: Performance & Testing

**Purpose**: Meet performance requirements and ensure quality

### Performance Tests

- [ ] T137 Create large_10k_lines.cpp test fixture in tests/integration/fixtures/
- [ ] T138 Performance test for 10k line file completing in <30 seconds in tests/integration/test_large_files.py (SC-001)
- [ ] T139 Performance test for memory usage staying <2GB with 1000 functions in tests/integration/test_large_files.py (SC-001a)
- [ ] T140 Benchmark test using pytest-benchmark for parser performance in tests/integration/test_large_files.py
- [ ] T141 Benchmark test using pytest-benchmark for grouper performance in tests/integration/test_large_files.py

### Optimization

- [ ] T142 Profile CppParser with cProfile to identify bottlenecks
- [ ] T143 Optimize CppParser with libclang flags (CXTranslationUnit_SingleFileParse)
- [ ] T144 Consider precompiled headers for standard library if needed
- [ ] T145 Profile memory usage with memory_profiler
- [ ] T146 Optimize CallGraph memory usage if needed (use compact representations)

### Quality Checks

- [ ] T147 Run ruff linter on all source code and fix issues
- [ ] T148 Run mypy type checker and achieve 100% type coverage
- [ ] T149 Run pytest with coverage and achieve >90% coverage
- [ ] T150 Test against real C++ project (e.g., nlohmann/json) to verify SC-005 (95% parse success)
- [ ] T151 Validate all exit codes work correctly
- [ ] T152 Validate all CLI options work correctly
- [ ] T153 Validate JSON output against schema
- [ ] T154 Validate DOT output is parseable by Graphviz

---

## Phase 9: Sample Generation & Verification (Constitution Principle IX)

**Purpose**: Generate representative C++ samples and verify tool functionality before marking implementation complete

**⚠️ CRITICAL**: This phase implements Constitution Principle IX (Sample-Driven Verification) - tasks MUST be completed before marking implementation done

### Sample Creation

- [X] T155 Create examples/ directory at repository root
- [X] T156 [P] Create examples/simple.cpp with 3-5 functions forming 2 independent groups
- [X] T157 [P] Create examples/complex.cpp with 10+ functions, circular dependencies, and templates
- [X] T158 [P] Create examples/edge_cases.cpp demonstrating recursion, overloads, and lambdas
- [X] T159 [P] Create examples/real_world.cpp extracted from actual C++ project (e.g., small utility from open-source code)

### Sample Verification - User Story 1 (Parsing & Grouping)

- [ ] T160 Run function-grouper on examples/simple.cpp and capture output
- [ ] T161 Verify examples/simple.cpp output correctly identifies 2 independent groups
- [ ] T162 Validate examples/simple.cpp JSON output against schema in contracts/
- [ ] T163 Save verified output as examples/simple_output.json
- [ ] T164 Save verified output as examples/simple_output.txt

### Sample Verification - User Story 2 (Visualization)

- [ ] T165 Run function-grouper -f json on examples/complex.cpp and verify JSON schema compliance
- [ ] T166 Run function-grouper -f dot on examples/complex.cpp and verify Graphviz can parse output
- [ ] T167 Generate visualization: dot -Tpng examples/complex_output.dot -o examples/complex_graph.png
- [ ] T168 Verify examples/complex.cpp correctly reports circular dependencies
- [ ] T169 Save verified outputs as examples/complex_output.json, examples/complex_output.txt, examples/complex_output.dot

### Sample Verification - User Story 3 (Export)

- [ ] T170 Run function-grouper --export-suggestions on examples/complex.cpp
- [ ] T171 Verify export suggestions include reasonable file names for each group
- [ ] T172 Verify export suggestions identify required headers for each group
- [ ] T173 Verify warnings about imbalanced groups appear when appropriate

### Sample Verification - Edge Cases

- [ ] T174 Run function-grouper on examples/edge_cases.cpp and verify recursion handling
- [ ] T175 Verify function overloads are correctly distinguished
- [ ] T176 Verify lambdas are correctly identified and grouped
- [ ] T177 Verify template functions are handled per FR-007

### Sample Documentation

- [X] T178 Create examples/README.md documenting all sample files
- [X] T179 Add to examples/README.md: purpose of each sample, expected behavior, how to run
- [X] T180 Add to examples/README.md: instructions for generating visualizations from DOT output
- [ ] T181 Add sample verification as step in integration tests (reuse samples in tests/integration/)

**Checkpoint**: All samples execute successfully, outputs are verified correct, edge cases handled properly

---

## Phase 10: Comprehensive Documentation (Constitution Principle VIII)

**Purpose**: Ensure README.md and documentation meet Constitution Principle VIII requirements

**⚠️ CRITICAL**: This phase implements Constitution Principle VIII (Comprehensive Documentation) - documentation MUST be comprehensive, maintained, and contain verified runnable samples

### README.md Enhancement

- [X] T182 Review existing README.md for completeness per Principle VIII checklist
- [X] T183 Add comprehensive installation section with pip install examples (verify runnable)
- [X] T184 Add basic usage section with simple examples (copy from verified examples/)
- [X] T185 Add advanced usage section demonstrating all output formats (JSON, text, DOT)
- [X] T186 Add section demonstrating include paths (-I flag) with real example
- [X] T187 Add section demonstrating C++ standard selection (--std flag)
- [X] T188 Add error handling examples showing graceful degradation
- [X] T189 Add performance characteristics section (10k lines in <30s, <2GB memory)
- [X] T190 Add troubleshooting section with common issues and solutions
- [X] T191 Add section documenting all success criteria from spec.md
- [X] T192 Verify ALL code samples in README.md are executable and produce shown results

### Troubleshooting Section Content

- [X] T193 Add troubleshooting entry: "File not found" → Check path, use absolute paths if needed
- [X] T194 Add troubleshooting entry: "Parse errors" → Try different --std version, check file is valid C++
- [X] T195 Add troubleshooting entry: "Memory exceeded" → File too large, try splitting analysis
- [X] T196 Add troubleshooting entry: "Slow parsing" → Check file size, disable progress for speed
- [X] T197 Add troubleshooting entry: "Missing functions" → Check include paths with -I flag

### Additional Documentation

- [ ] T198 [P] Update CONTRIBUTING.md with development workflow, TDD requirements, and constitution compliance
- [X] T199 [P] Create examples section in README.md linking to examples/ directory
- [X] T200 [P] Add output format examples to README.md (JSON, text, DOT) using verified samples
- [X] T201 [P] Add "Features" section to README.md listing all capabilities from spec.md
- [X] T202 [P] Add "Limitations" section to README.md documenting known edge cases
- [X] T203 Verify documentation stays synchronized with code (all features documented, no outdated examples)

**Checkpoint**: README.md is comprehensive, all samples verified runnable, troubleshooting complete

---

## Phase 11: CI/CD & Automation

**Purpose**: Continuous integration and automated quality checks

- [ ] T204 [P] Create GitHub Actions workflow in .github/workflows/ci.yml
- [ ] T205 [P] Add CI job for running pytest with coverage
- [ ] T206 [P] Add CI job for running ruff linter
- [ ] T207 [P] Add CI job for running mypy type checker
- [ ] T208 [P] Add CI job for testing on Linux, macOS, Windows
- [ ] T209 [P] Add CI job for testing Python 3.11, 3.12
- [ ] T210 [P] Add CI job for verifying all examples/ samples execute successfully
- [ ] T211 [P] Add CI job for verifying README.md code samples are runnable
- [ ] T212 [P] Update CLAUDE.md with final project commands

---

## Phase 12: Polish & Final Validation

**Purpose**: Final improvements and validation against quickstart.md

- [ ] T213 Run all validation steps from quickstart.md
- [ ] T214 Test TDD workflow from quickstart.md works correctly
- [ ] T215 Verify all success criteria from spec.md are met
- [ ] T216 Run full test suite and ensure 100% passing
- [ ] T217 Generate final coverage report
- [ ] T218 Create demo run with real C++ file and showcase all formats
- [ ] T219 Review and clean up any TODO comments in code
- [ ] T220 Final code review for code quality and constitution compliance
- [ ] T221 Verify constitution compliance (all 9 principles including VIII and IX)
- [ ] T222 Verify zero warnings from ruff and mypy
- [ ] T223 Tag version 1.0.0 release

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational completion - Core MVP
- **User Story 2 (Phase 4)**: Depends on Foundational completion - Can start in parallel with US1 but logically follows
- **User Story 3 (Phase 5)**: Depends on US1 completion (needs grouping analysis)
- **CLI Integration (Phase 6)**: Depends on US1, US2, US3 completion
- **Progress & Error Handling (Phase 7)**: Depends on CLI integration
- **Performance & Testing (Phase 8)**: Depends on complete implementation
- **Sample Generation & Verification (Phase 9)**: Depends on Phases 3-7 - REQUIRED before marking implementation complete (Constitution Principle IX)
- **Comprehensive Documentation (Phase 10)**: Depends on Phase 9 samples - REQUIRED documentation quality (Constitution Principle VIII)
- **CI/CD & Automation (Phase 11)**: Can proceed once core implementation and samples are stable
- **Polish (Phase 12)**: Depends on all previous phases

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories - **MVP TARGET**
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Builds on US1's analysis to add visualization
- **User Story 3 (P3)**: Depends on US1 completion - Uses grouping results to suggest exports

### Within Each User Story

- Tests MUST be written FIRST and FAIL before implementation
- Models before services/logic
- Core functionality before integration
- Story complete and tested before moving to next priority

### Parallel Opportunities

#### Phase 1 (Setup)
- T003-T010 can all run in parallel (different files)

#### Phase 2 (Foundational)
- T011-T012 can run in parallel (enums in same file but independent)
- T015, T017, T018 can run in parallel (different model files)
- T020-T023 can run in parallel (test fixtures)

#### Phase 3 (User Story 1) - Tests
- T024-T031 can all run in parallel (different test files)

#### Phase 3 (User Story 1) - Implementation
- T032-T033 can run in parallel (different files)
- T041-T042 can run in parallel (different modules)
- T044-T045 can run in parallel (methods in same class)

#### Phase 4 (User Story 2) - Tests
- T058-T063 can all run in parallel (different test files)

#### Phase 4 (User Story 2) - Implementation
- T064-T066 can run in parallel (different formatter files)

#### Phase 6 (CLI) - Tests
- T095-T101 can all run in parallel (different test scenarios)

#### Phase 6 (CLI) - Options
- T104-T115 can run in parallel (independent options)

#### Phase 9 (Sample Creation)
- T156-T159 can run in parallel (different sample files)

#### Phase 10 (Documentation)
- T183-T192 can run in parallel (different documentation sections)
- T193-T197 can run in parallel (different troubleshooting entries)
- T198-T202 can run in parallel (different documentation files)

#### Phase 11 (CI/CD)
- T204-T212 can all run in parallel (different CI jobs and documentation files)

---

## Parallel Example: Phase 3 User Story 1

```bash
# Launch all test creation tasks in parallel:
Task: "Unit test for CppParser.parse_file() with simple function in tests/unit/test_parser.py"
Task: "Unit test for CppParser extracting function names and signatures in tests/unit/test_parser.py"
Task: "Unit test for CppParser identifying function calls in tests/unit/test_parser.py"
Task: "Unit test for CallGraph.add_function() in tests/unit/test_analyzer.py"
Task: "Unit test for CallGraph.add_call() in tests/unit/test_analyzer.py"
Task: "Unit test for Grouper.find_connected_components() in tests/unit/test_grouper.py"
Task: "Integration test for end-to-end analysis with simple_independent.cpp in tests/integration/test_end_to_end.py"
Task: "Integration test for end-to-end analysis with complex_dependencies.cpp in tests/integration/test_end_to_end.py"

# Then launch parser and analyzer class creation in parallel:
Task: "Create CppParser class skeleton in src/function_grouper/parser/cpp_parser.py"
Task: "Create FunctionExtractor helper class in src/function_grouper/parser/function_extractor.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T010)
2. Complete Phase 2: Foundational (T011-T023) - CRITICAL - blocks all stories
3. Complete Phase 3: User Story 1 (T024-T057) - Core parsing, analysis, grouping
4. Complete Phase 6: Basic CLI (T102-T121) - Minimal CLI to run US1
5. **STOP and VALIDATE**: Test User Story 1 independently with CLI
6. Can already deliver value: analyze C++ files and identify independent groups!

### Incremental Delivery

1. **Foundation** (Phases 1-2) → Project structure ready
2. **MVP** (Phase 3 + basic Phase 6) → Can analyze and group functions (text output)
3. **Enhanced Visualization** (Phase 4) → Add JSON and DOT formats
4. **Export Suggestions** (Phase 5) → Add file split recommendations
5. **UX Polish** (Phase 7) → Add progress bars and better error handling
6. **Performance** (Phase 8) → Optimize and validate against requirements
7. **Sample Verification** (Phase 9) → Generate samples and verify functionality (Constitution Principle IX)
8. **Documentation Quality** (Phase 10) → Comprehensive README with runnable examples (Constitution Principle VIII)
9. **Production Ready** (Phases 11-12) → CI/CD, automation, final polish

Each increment adds value without breaking previous functionality.

**IMPORTANT**: Phases 9-10 are REQUIRED by constitution v1.1.0 before marking implementation complete.

### Parallel Team Strategy

With multiple developers after Foundational phase completes:

1. Developer A: User Story 1 core implementation (T024-T057)
2. Developer B: User Story 2 formatters (T058-T083) - can start parser work independently
3. Developer C: CLI integration (T095-T121) - can stub out while waiting for US1/US2
4. Stories integrate at Phase 6 completion

---

## Notes

- **TDD Required**: All tests must be written FIRST and FAIL before implementation (per constitution)
- **[P] marker**: Tasks that can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story] label**: Maps task to specific user story (US1, US2, US3) for traceability
- **File paths**: All tasks include exact file paths for clarity
- **Independent testing**: Each user story has clear test criteria and can be validated independently
- **Graceful degradation**: Parser continues with partial analysis on errors (FR-014)
- **Performance targets**: 10k lines in <30s, <2GB memory (SC-001, SC-001a)
- **Constitution compliance**: Zero warnings (ruff, mypy), 100% test pass, TDD workflow
- **Commit frequently**: After each task or logical group of tasks
- **Stop at checkpoints**: Validate story independently before proceeding

---

## Summary Statistics

- **Total Tasks**: 223 tasks (was 175, added 48 for Principles VIII & IX)
- **Phase 1 (Setup)**: 10 tasks (8 parallelizable)
- **Phase 2 (Foundational)**: 13 tasks (10 parallelizable)
- **Phase 3 (US1 - MVP)**: 34 tasks (8 test tasks, 26 implementation tasks)
- **Phase 4 (US2 - Visualization)**: 26 tasks (6 test tasks, 20 implementation tasks)
- **Phase 5 (US3 - Export)**: 11 tasks (3 test tasks, 8 implementation tasks)
- **Phase 6 (CLI)**: 27 tasks (7 test tasks, 20 implementation tasks)
- **Phase 7 (Progress/Errors)**: 15 tasks
- **Phase 8 (Performance)**: 18 tasks
- **Phase 9 (Sample Verification - NEW)**: 27 tasks (Constitution Principle IX - sample-driven verification)
- **Phase 10 (Documentation - NEW)**: 22 tasks (Constitution Principle VIII - comprehensive documentation)
- **Phase 11 (CI/CD)**: 9 tasks (all parallelizable, includes sample/doc verification)
- **Phase 12 (Polish)**: 11 tasks (includes constitution compliance check)

**Parallel Opportunities Identified**: 70+ tasks can run in parallel within their phases

**Constitution Compliance**:
- **Principle VIII (Comprehensive Documentation)**: Phase 10 - 22 tasks ensuring README quality
- **Principle IX (Sample-Driven Verification)**: Phase 9 - 27 tasks for sample generation and verification
- These phases are REQUIRED before marking implementation complete

**MVP Scope (Recommended First Delivery)**:
- Phases 1-3 + basic Phase 6 = ~57 tasks
- Delivers: Parse C++ files, identify independent function groups, output results
- Validates core value proposition before investing in additional features
- **NOTE**: Phases 9-10 MUST be completed before final release per constitution v1.1.0

**Independent Test Criteria**:
- US1: Analyze files with known dependencies, verify correct grouping (100% accuracy required)
- US2: Verify output formats are valid, readable, and complete (schema compliance)
- US3: Verify export suggestions are logical and include necessary information
- **Sample Verification (NEW)**: All examples/ samples execute successfully and produce expected results
- **Documentation Quality (NEW)**: All README.md code samples are verified runnable
