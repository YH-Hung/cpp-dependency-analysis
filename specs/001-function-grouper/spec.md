# Feature Specification: C++ Function Grouper

**Feature Branch**: `001-function-grouper`
**Created**: 2025-10-25
**Status**: Draft
**Input**: User description: "an utility that can separate functions in a large c++ files into several independent groups. what i mean independent is that they did not reference each other."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Analyze Function Independence (Priority: P1)

A developer has a large C++ file with many functions and wants to understand which functions are independent (do not call each other) so they can reorganize the code more effectively.

**Why this priority**: This is the core value proposition - analyzing and identifying independent function groups. Without this, the feature cannot deliver any value.

**Independent Test**: Can be fully tested by providing a C++ file with known function dependencies and verifying the tool correctly identifies all independent groups.

**Acceptance Scenarios**:

1. **Given** a C++ file with 5 functions where 3 functions are independent and 2 functions call each other, **When** the user runs the analysis, **Then** the tool identifies 2 groups: one with 3 independent functions and one with 2 interdependent functions.

2. **Given** a C++ file where all functions are completely independent, **When** the user runs the analysis, **Then** the tool identifies each function as its own group.

3. **Given** a C++ file where all functions form a call chain (A→B→C), **When** the user runs the analysis, **Then** the tool identifies one group containing all functions.

4. **Given** a C++ file with function templates and overloaded functions, **When** the user runs the analysis, **Then** the tool correctly distinguishes between different overloads and template instantiations.

---

### User Story 2 - Visualize Function Relationships (Priority: P2)

A developer wants to see a clear visualization or report of which functions call which other functions to understand the dependency structure before refactoring.

**Why this priority**: Visualization helps developers understand complex dependencies and plan refactoring strategies. This builds on P1 but isn't essential for the core grouping functionality.

**Independent Test**: Can be tested by running the tool on a known file and verifying the output format clearly shows function relationships.

**Acceptance Scenarios**:

1. **Given** a C++ file with complex function dependencies, **When** the user requests a dependency report, **Then** the tool outputs a readable format showing which functions call which other functions.

2. **Given** a C++ file analyzed for independence, **When** the user views the results, **Then** each group is clearly labeled with the functions it contains.

3. **Given** a C++ file with circular dependencies (A→B→A), **When** the user runs the analysis, **Then** the tool identifies the circular dependency and reports it clearly.

---

### User Story 3 - Export Grouped Functions (Priority: P3)

A developer wants to export or suggest file splits based on the independent function groups to facilitate actual code refactoring.

**Why this priority**: This is a convenience feature that builds on P1 and P2. The core analysis can be done without automated export.

**Independent Test**: Can be tested by analyzing a file, requesting export suggestions, and verifying the suggestions make logical sense based on the grouping.

**Acceptance Scenarios**:

1. **Given** a C++ file with 3 independent groups identified, **When** the user requests export suggestions, **Then** the tool suggests splitting into 3 separate files with appropriate names.

2. **Given** a C++ file with function groups and header dependencies, **When** the user requests export, **Then** the tool identifies which header includes each group requires.

3. **Given** a C++ file where one group is much larger than others, **When** the user reviews export suggestions, **Then** the tool highlights this imbalance for user consideration.

---

### Edge Cases

- What happens when a file contains no functions (empty file, only declarations)?
- How does the system handle function pointers and callbacks?
- What happens with macro-based function calls?
- How are indirect dependencies handled (A calls B, B calls C, but A never directly calls C)?
- What happens with static functions vs. non-static functions?
- How does the tool handle inline functions?
- What happens when a function calls itself (recursion)?
- How are template functions with different instantiations handled?
- What happens with functions that only differ by namespace?
- How does the tool handle operator overloading?
- What happens when the parser encounters unparseable code (complex macros, compiler extensions)?
- How does the tool report partial analysis results when some functions fail to parse?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST parse C++ source files and identify all function definitions.

- **FR-002**: System MUST analyze function call relationships to determine which functions call which other functions within the same file.

- **FR-003**: System MUST identify groups of functions that are completely independent (no function in group A calls any function in group A).

- **FR-004**: System MUST handle multiple levels of indirect dependencies (if A calls B and B calls C, then A, B, and C are in the same dependency group).

- **FR-005**: System MUST distinguish between function calls within the file and calls to external functions (library functions, functions from other files).

- **FR-006**: System MUST handle function overloading correctly (treat each overload as a separate function based on signature).

- **FR-007**: System MUST handle function templates and correctly identify dependencies based on template usage.

- **FR-008**: System MUST detect and report circular dependencies within the file.

- **FR-009**: System MUST handle both member functions (methods) and free functions.

- **FR-010**: System MUST produce output showing the identified independent groups with clear group labels.

- **FR-010a**: System MUST support multiple output formats: JSON (structured data), plain text (human-readable), and DOT (Graphviz visualization), selectable via command-line flags.

- **FR-011**: System MUST handle recursive functions (functions that call themselves) by placing them in appropriate dependency groups.

- **FR-012**: System MUST accept C++ implementation files (.cpp) as input.

- **FR-013**: System MUST handle modern C++ features including lambdas, auto return types, and constexpr functions.

- **FR-014**: System MUST continue analysis when encountering unparseable functions, analyze all parseable functions, and report which functions could not be parsed with specific error messages.

- **FR-015**: System MUST display progress indication during analysis, showing percentage complete and current processing phase (parsing, analyzing, or outputting).

### Assumptions

- The tool targets syntactically correct C++ code, but will gracefully handle parse errors by continuing with partial analysis.
- The tool will focus on direct function calls visible in the source; it will not analyze function pointer calls or virtual function dispatch.
- The tool will treat template instantiations as separate functions only if they appear in the analyzed file.
- For scope, we assume C++17 as the baseline with optional C++20 support.

### Key Entities

- **Function**: Represents a function definition in the C++ file with attributes including name, signature, location, and call list.

- **Function Group**: Represents a collection of functions that are connected through direct or indirect call relationships, with independence status.

- **Call Relationship**: Represents a directed edge from one function (caller) to another function (callee), capturing the dependency.

- **Dependency Graph**: The complete graph structure representing all functions as nodes and call relationships as edges, used to compute independent groups.

## Clarifications

### Session 2025-10-25

- Q: Performance target for large files (hundreds of functions, 10k+ lines common) → A: Increase to 10,000 lines in under 30 seconds (matches typical use case)
- Q: Output format for large results (hundreds of functions) → A: Multiple formats: JSON, text, and DOT available via flags (most flexible)
- Q: Memory limit for large file analysis → A: Maximum 2GB memory usage (prevents system exhaustion, handles large files)
- Q: Handling parse errors in real-world files → A: Continue with partial analysis, report which functions couldn't be parsed (graceful degradation)
- Q: Progress indication for long-running analysis → A: Show progress percentage and current phase (parsing/analyzing/outputting)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can analyze a 10,000-line C++ file and receive complete grouping results in under 30 seconds.

- **SC-001a**: The tool MUST not exceed 2GB of memory usage during analysis, even for files with 1000 functions.

- **SC-002**: The tool correctly identifies independent function groups with 100% accuracy on files with known dependencies (validated through test suite).

- **SC-003**: The tool handles C++ files with up to 1000 function definitions without errors or crashes.

- **SC-004**: Users can understand the output format without referring to documentation (clear, self-explanatory group labels and structure).

- **SC-005**: The tool successfully parses and analyzes at least 95% of real-world C++ projects without syntax errors (tested on open-source codebases).

- **SC-006**: Developers reduce time spent manually analyzing function dependencies by at least 80% compared to manual code review.
