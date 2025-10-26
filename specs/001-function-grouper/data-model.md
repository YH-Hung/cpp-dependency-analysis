# Data Model: C++ Function Grouper

## Overview

This document defines the data structures used in the C++ Function Grouper tool. The system analyzes C++ source files to build dependency graphs and identify independent function groups.

## Core Entities

### 1. Function

Represents a single function definition found in the C++ source file.

**Attributes**:
- `name: str` - Function name (e.g., `calculateTotal`)
- `qualified_name: str` - Fully qualified name including namespace/class (e.g., `MyNamespace::MyClass::calculateTotal`)
- `signature: str` - Function signature including parameters and return type
- `location: SourceLocation` - Source file location (file path, line number, column number)
- `kind: FunctionKind` - Type of function (free function, member function, static member, etc.)
- `calls: List[str]` - List of qualified names of functions called by this function
- `parse_status: ParseStatus` - Whether the function was successfully parsed

**Validation Rules**:
- `name` must be non-empty
- `qualified_name` must be unique within a file
- `location.line_number` must be positive
- `calls` list may be empty (for functions that don't call other functions)

**Relationships**:
- A Function can call multiple other Functions (many-to-many via `calls` list)
- A Function belongs to exactly one SourceFile
- A Function belongs to zero or more FunctionGroups

**State Transitions**: None (immutable after parsing)

### 2. SourceLocation

Represents the position of a function in the source code.

**Attributes**:
- `file_path: str` - Absolute path to the source file
- `line_number: int` - Line number where function definition starts (1-indexed)
- `column_number: int` - Column number where function definition starts (1-indexed)
- `end_line_number: int | None` - Line number where function definition ends (optional)

**Validation Rules**:
- `file_path` must exist and be readable
- `line_number` >= 1
- `column_number` >= 1
- `end_line_number` >= `line_number` (if provided)

### 3. FunctionKind (Enum)

Categorizes the type of function definition.

**Values**:
- `FREE_FUNCTION` - Standalone function not part of a class
- `MEMBER_FUNCTION` - Non-static class member function (method)
- `STATIC_MEMBER_FUNCTION` - Static class member function
- `CONSTRUCTOR` - Class constructor
- `DESTRUCTOR` - Class destructor
- `OPERATOR` - Overloaded operator
- `LAMBDA` - Lambda function
- `TEMPLATE_FUNCTION` - Template function definition
- `TEMPLATE_SPECIALIZATION` - Template specialization

**Usage**: Used to distinguish different function types for analysis and reporting purposes.

### 4. ParseStatus (Enum)

Indicates the parsing result for a function.

**Values**:
- `SUCCESS` - Function was successfully parsed
- `PARTIAL` - Function was parsed but with warnings or missing information
- `FAILED` - Function could not be parsed (syntax error, unsupported feature, etc.)

**Attributes (when status is FAILED or PARTIAL)**:
- `error_message: str | None` - Description of the parsing issue

### 5. CallGraph

Represents the complete directed graph of function call relationships within a file.

**Attributes**:
- `functions: Dict[str, Function]` - Map of qualified_name -> Function object
- `edges: List[CallEdge]` - List of directed edges representing function calls
- `metadata: GraphMetadata` - Metadata about the graph (file info, parsing stats)

**Methods**:
- `add_function(func: Function) -> None` - Add a function node to the graph
- `add_call(caller: str, callee: str) -> None` - Add a directed edge from caller to callee
- `get_callers(func_name: str) -> List[str]` - Get all functions that call the specified function
- `get_callees(func_name: str) -> List[str]` - Get all functions called by the specified function
- `has_cycle() -> bool` - Check if the call graph contains cycles
- `find_cycles() -> List[List[str]]` - Return all cycles in the graph

**Validation Rules**:
- All edges must reference functions that exist in the `functions` dict
- No self-loops are allowed unless explicitly representing recursion

**Relationships**:
- Contains multiple Function objects
- Contains multiple CallEdge objects connecting Functions

### 6. CallEdge

Represents a single directed edge in the call graph (caller → callee).

**Attributes**:
- `caller: str` - Qualified name of the calling function
- `callee: str` - Qualified name of the called function
- `call_count: int` - Number of times caller invokes callee (optional, defaults to 1)
- `call_locations: List[SourceLocation]` - Locations where the calls occur

**Validation Rules**:
- `caller` and `callee` must be non-empty
- `call_count` >= 1
- `caller` != `callee` (unless representing recursion)

### 7. FunctionGroup

Represents a collection of functions that are connected through direct or indirect call relationships.

**Attributes**:
- `group_id: int` - Unique identifier for this group
- `functions: List[str]` - List of qualified function names in this group
- `is_independent: bool` - True if this group has no calls to/from other groups
- `internal_edges: int` - Number of call edges within the group
- `external_edges: int` - Number of call edges to/from other groups
- `has_cycles: bool` - Whether this group contains circular dependencies

**Validation Rules**:
- `group_id` must be unique across all groups in the analysis
- `functions` list must be non-empty
- `internal_edges` >= 0
- `external_edges` >= 0
- If `is_independent` is True, then `external_edges` must be 0

**Relationships**:
- Contains multiple Function objects (via qualified name references)
- May have dependencies on other FunctionGroups (via external_edges)

**Grouping Algorithm**:
- Groups are computed using connected components algorithm on the undirected version of the call graph
- Functions in the same group are reachable from each other through some path of function calls

### 8. GraphMetadata

Contains summary information about the parsed file and resulting call graph.

**Attributes**:
- `source_file: str` - Path to the analyzed .cpp file
- `parse_timestamp: datetime` - When the analysis was performed
- `total_functions: int` - Total number of functions found
- `successfully_parsed: int` - Number of functions parsed successfully
- `failed_to_parse: int` - Number of functions that couldn't be parsed
- `total_call_edges: int` - Total number of function call relationships identified
- `total_groups: int` - Number of function groups identified
- `independent_groups: int` - Number of groups with no external dependencies
- `largest_group_size: int` - Size of the largest function group
- `analysis_duration_seconds: float` - Time taken for analysis
- `memory_used_mb: float` - Peak memory usage during analysis

**Usage**: Used for reporting and validating success criteria (performance, accuracy).

## Data Flow

1. **Parsing Phase**:
   - Input: C++ source file (.cpp)
   - Output: List of `Function` objects with populated attributes

2. **Graph Construction Phase**:
   - Input: List of `Function` objects
   - Output: `CallGraph` with all `CallEdge` objects connecting functions

3. **Grouping Phase**:
   - Input: `CallGraph`
   - Output: List of `FunctionGroup` objects representing independent/dependent clusters

4. **Output Phase**:
   - Input: `CallGraph`, List of `FunctionGroup`, `GraphMetadata`
   - Output: JSON/Text/DOT formatted results

## Example Data Instance

```python
# Example Function
func1 = Function(
    name="processData",
    qualified_name="DataProcessor::processData",
    signature="void DataProcessor::processData(const std::string& input)",
    location=SourceLocation(
        file_path="/path/to/file.cpp",
        line_number=42,
        column_number=5,
        end_line_number=58
    ),
    kind=FunctionKind.MEMBER_FUNCTION,
    calls=["DataProcessor::validate", "DataProcessor::transform"],
    parse_status=ParseStatus.SUCCESS
)

# Example CallEdge
edge = CallEdge(
    caller="DataProcessor::processData",
    callee="DataProcessor::validate",
    call_count=1,
    call_locations=[SourceLocation("/path/to/file.cpp", 45, 12, None)]
)

# Example FunctionGroup
group = FunctionGroup(
    group_id=1,
    functions=[
        "DataProcessor::processData",
        "DataProcessor::validate",
        "DataProcessor::transform"
    ],
    is_independent=True,
    internal_edges=2,
    external_edges=0,
    has_cycles=False
)
```

## Performance Considerations

**Memory Estimates**:
- Each Function: ~500 bytes (with name, signature, calls list)
- 1000 functions: ~500 KB
- Call edges (sparse graph, avg 3 calls/function): 1000 × 3 × 50 bytes = ~150 KB
- Total for 1000 functions: < 1 MB

**For 10,000-line files with 1000 functions**: Memory usage should be well under 100 MB, leaving significant headroom before the 2GB limit.

**Graph Algorithm Complexity**:
- Building graph: O(N) where N = number of functions
- Finding connected components: O(V + E) where V = vertices (functions), E = edges (calls)
- Cycle detection: O(V + E) using DFS

All operations are linear or near-linear, suitable for the target scale (1000 functions).

## Data Validation

**Input Validation** (during parsing):
- File exists and is readable
- File size < 100MB (sanity check)
- Function names are valid C++ identifiers

**Internal Consistency Validation** (after graph construction):
- All call edges reference existing functions
- Group partitioning is complete (every function in exactly one group)
- Group independence flags match actual edge counts
- Metadata counts match actual data (total_functions == len(functions))

**Output Validation** (before formatting):
- JSON schema compliance
- DOT format syntax validity
- Text output readability checks
