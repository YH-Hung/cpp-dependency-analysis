# C++ Function Grouper - Example Files

This directory contains sample C++ files demonstrating the C++ Function Grouper tool's capabilities. Each file is designed to test specific features and edge cases.

## Sample Files

### 1. simple.cpp

**Purpose**: Basic example demonstrating independent function groups.

**Contents**:
- 3 functions total
- 2 independent groups:
  - **Group 1**: `helper()` and `process()` (connected via function call)
  - **Group 2**: `independentFunction()` (standalone)

**Expected Behavior**:
- Tool should identify 2 groups
- Group 1 should contain 2 functions with 1 internal call
- Group 2 should contain 1 function with 0 calls

**How to Run**:
```bash
# Default text output
function-grouper examples/simple.cpp

# JSON output
function-grouper -f json -o examples/simple_output.json examples/simple.cpp

# DOT output for visualization
function-grouper -f dot -o examples/simple_output.dot examples/simple.cpp
dot -Tpng examples/simple_output.dot -o examples/simple_graph.png
```

---

### 2. complex.cpp

**Purpose**: Advanced example with circular dependencies, templates, overloading, and larger function graphs.

**Contents**:
- 15+ functions
- 5 independent groups:
  - **Group 1**: `functionA()` and `functionB()` (circular dependency)
  - **Group 2**: `add()` and `multiply()` template functions (template calls)
  - **Group 3**: Three `process()` overloads (overloaded functions)
  - **Group 4**: `functionC()`, `functionD()`, `functionE()` (call chain)
  - **Group 5**: `standaloneComplex()` (independent)

**Expected Behavior**:
- Tool should identify 5 groups
- Group 1 should detect circular dependency
- Template functions should be grouped together
- Overloaded functions should be treated as separate entities
- Call chain should form connected component

**How to Run**:
```bash
# Analyze with JSON output to see detailed structure
function-grouper -f json examples/complex.cpp

# Generate visualization showing circular dependencies
function-grouper -f dot examples/complex.cpp | dot -Tpng > examples/complex_graph.png

# Text output with all details
function-grouper -vv examples/complex.cpp
```

---

### 3. edge_cases.cpp

**Purpose**: Test special C++ features and boundary conditions.

**Contents**:
- Recursive functions (`factorial()`)
- Mutual recursion (`isEven()` ↔ `isOdd()`)
- Function overloads (multiple `print()` signatures)
- Lambda expressions
- Operator overloading (class `Counter`)
- Callback functions
- Static member functions
- Inline functions

**Expected Behavior**:
- Recursive functions should be in their own group (self-loop)
- Mutually recursive functions should be grouped together
- Overloaded functions should be distinguished by signature
- Lambda expressions should be detected
- Member functions and static functions should be handled correctly

**How to Run**:
```bash
# Analyze recursion patterns
function-grouper examples/edge_cases.cpp

# Check for circular dependencies (mutual recursion)
function-grouper -f json examples/edge_cases.cpp | grep -A5 "has_cycles"

# Verbose output showing all function kinds
function-grouper -vv examples/edge_cases.cpp
```

---

### 4. real_world.cpp

**Purpose**: Realistic example extracted from actual C++ utility code - string manipulation library.

**Contents**:
- 17 functions organized into 5 logical groups:
  - **Group 1**: Trimming utilities (`isWhitespace()`, `trimLeft()`, `trimRight()`, `trim()`)
  - **Group 2**: Splitting utilities (`split()`, `join()`)
  - **Group 3**: Case conversion (`toLowerCase()`, `toUpperCase()`)
  - **Group 4**: Validation (`startsWith()`, `endsWith()`, `contains()`)
  - **Group 5**: Replacement (`replace()` - uses `contains()` from Group 4)

**Expected Behavior**:
- Tool should identify 4-5 groups (Group 5 depends on Group 4)
- Groups 1, 2, 3 should be fully independent
- Group 4 and 5 may be combined if `replace()` calls `contains()`
- Demonstrates realistic refactoring opportunity (separate file per group)

**How to Run**:
```bash
# Analyze the dependency structure
function-grouper examples/real_world.cpp

# Export suggestions for file splitting
function-grouper --export-suggestions examples/real_world.cpp

# JSON output for programmatic processing
function-grouper -f json -o examples/real_world_output.json examples/real_world.cpp
```

---

## Visualizing Results

To generate visual graphs of function dependencies:

```bash
# 1. Generate DOT file
function-grouper -f dot -o graph.dot examples/<file>.cpp

# 2. Convert to PNG using Graphviz
dot -Tpng graph.dot -o graph.png

# 3. View the image
open graph.png  # macOS
xdg-open graph.png  # Linux
```

## Expected Outputs

After running the tool on these examples, you should see:

- **simple.cpp**: 2 groups, 3 functions, 1 call relationship
- **complex.cpp**: 5 groups, 15+ functions, circular dependencies detected
- **edge_cases.cpp**: Multiple groups with recursion and special features
- **real_world.cpp**: 4-5 groups showing realistic refactoring opportunities

## Validation

These sample files are used for:

1. **Integration testing**: Verify tool correctness against known inputs
2. **Documentation**: Demonstrate tool capabilities to users
3. **Constitution compliance**: Satisfy Principle IX (sample-driven verification)

All samples should execute successfully and produce expected groupings as described above.

## Troubleshooting

**Issue**: Tool fails to parse template functions
- **Solution**: Try using `--std c++17` or `--std c++20` flag

**Issue**: Some functions not detected
- **Solution**: Ensure file is valid C++ and includes function bodies (not just declarations)

**Issue**: Unexpected grouping
- **Solution**: Use `-vv` flag for verbose output to see detailed function call analysis

## Notes

- All sample files are standalone and do not require external headers beyond standard library
- Files are designed to parse cleanly with C++11, C++17, and C++20 standards
- Sample complexity increases from simple.cpp (beginner) to real_world.cpp (realistic usage)
