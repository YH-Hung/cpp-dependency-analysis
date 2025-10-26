# C++ Parser Library Research for AST-based Dependency Analyzer

## Executive Summary

This document compares four Python libraries for parsing C++ source code to build an AST-based function dependency analyzer: tree-sitter with tree-sitter-cpp, libclang (clang Python bindings), pycparser, and CppHeaderParser/cxxheaderparser.

**Recommendation: Use libclang (via the `libclang` PyPI package)**

libclang provides the best combination of complete C++17/C++20 support, mature AST representation, cross-platform availability, and active maintenance. While tree-sitter offers superior performance for incremental parsing scenarios, libclang's semantic understanding and comprehensive language support make it the better choice for dependency analysis.

---

## 1. tree-sitter with tree-sitter-cpp

### Maintenance Status
- **Last Release**: v0.23.4 (November 11, 2024)
- **Activity**: Actively maintained with 439 total commits
- **Community**: Active with Discord/Matrix channels, multiple language bindings
- **Package Ecosystem**: Available on PyPI, npm, crates.io with regular updates

### C++ Version Support
- **C++11**: Good support for most features
- **C++17**: Partial support, undocumented which features are fully supported
- **C++20**: Incomplete support
  - C++20 modules are NOT supported
  - C++ concepts with `requires` clauses cause parsing errors
  - Template-related features have known issues
- **Documentation Gap**: No clear documentation of which C++ standard versions are fully supported

### Installation & Dependencies
```bash
pip install tree-sitter tree-sitter-cpp
# OR use the convenience package with all languages:
pip install tree-sitter-languages
```

**Platform Support**:
- Pre-compiled wheels for Windows (ARM64, x86-64)
- macOS (10.9+ x86-64, 11.0+ ARM64)
- Linux (manylinux 2.17+ x86-64/ARM64, musllinux 1.2+ x86-64)
- Requires Python 3.9+
- No C compiler needed for installation (binary wheels available)
- Cross-platform: ✅ Excellent

### Performance Characteristics
- **Speed**: Extremely fast - responds in milliseconds
- **Initial Parse**: Tens of milliseconds for typical large files
- **Incremental Updates**: Sub-millisecond for subsequent edits
- **Benchmark**: 36x speedup reported in migration from JavaParser to tree-sitter
- **10k Line Files**: Should parse in under 50ms (estimated based on benchmarks)
- **Optimization**: Designed for real-time, incremental parsing in editors

### Ease of Extracting Function Definitions and Calls
- **Approach**: Query-based pattern matching using S-expressions
- **Function Definitions**:
  ```python
  query = "(function_definition declarator: [(reference_declarator (function_declarator declarator: (_) @name)) (function_declarator declarator: (_) @name)])"
  ```
- **Function Calls**:
  ```python
  query = "(call_expression function: (identifier) @the-function arguments: (arguments) @args)"
  ```
- **Learning Curve**: Moderate - requires understanding tree-sitter query syntax
- **AST Type**: Concrete Syntax Tree (CST), not true AST
- **Ease Rating**: 7/10 - Powerful but requires learning query language

### Known Limitations
1. **Syntax-Only Parsing**: Creates only concrete syntax trees, cannot identify:
   - Virtual function identifiers
   - Global variable identifiers
   - Type information and semantic context
2. **Preprocessor Challenges**: Struggles with complex preprocessor directives
3. **Template Ambiguities**: Cannot fully resolve template-related parsing ambiguities (fundamentally undecidable without type information)
4. **Context-Insensitive**: No distinction between function declarations and constructor calls
5. **Error Tolerance**: May accept invalid syntax without marking parse trees as bad
6. **C++20 Modules**: Not supported
7. **Concepts & Requires**: Parsing errors with modern template features

### Use Case Fit
- **Best For**: Syntax highlighting, structural editing, code navigation
- **Not Ideal For**: Semantic analysis, type resolution, compiler-like analysis
- **Dependency Analysis**: Limited - can identify function call syntax but not resolve overloads, templates, or virtual functions

---

## 2. libclang (Python Bindings)

### Maintenance Status
- **Last Release**: 18.1.1 (March 17, 2024)
- **Activity**: Actively maintained with automated weekly updates when LLVM releases new versions
- **Community**: Large user base - 215,039 weekly downloads on PyPI
- **Backing**: Part of the official LLVM project
- **Maintenance**: 2025 refresh of build process confirms ongoing support

### C++ Version Support
- **C++11**: Full support
- **C++14**: Full support
- **C++17**: Full support (Clang 16+ defaults to C++17)
- **C++20**: Most features implemented (Clang 17+)
- **C++23**: Initial support available
- **Standard Compliance**: Tracks latest LLVM/Clang compiler releases
- **Best-in-class** for modern C++ standard support

### Installation & Dependencies
```bash
pip install libclang
```

**Platform Support**:
- Windows (x86-64, ARM64)
- macOS (10.9+ x86-64, 11.0+ ARM64)
- Linux (manylinux2010 x86-64, manylinux2014 aarch64/armv7l)
- Alpine Linux (musllinux 1.2+ x86-64)
- Python 2.7, 3.3-3.12 supported
- **Key Advantage**: Bundles static-linked libclang library - no external LLVM installation required
- Cross-platform: ✅ Excellent (batteries included)

**Note**: The `clang` package on PyPI contains only Python bindings without the library, requiring separate libclang installation. Use the `libclang` package instead.

### Performance Characteristics
- **Speed**: Moderate - slower than tree-sitter, faster than full compilation
- **Initial Parse**: Can range from <1 second to 30+ seconds depending on configuration
- **Optimization Techniques**:
  - Use precompiled headers to cache standard library headers
  - Flags: `CXTranslationUnit_SkipFunctionBodies`, `CXTranslationUnit_SingleFileParse`
  - Memory efficient: Historically used 1/6 of GCC's memory (2007 benchmarks)
- **10k Line Files**: 1-5 seconds estimated (highly dependent on includes and optimization)
- **Parallelization**: Each translation unit must be parsed separately

### Ease of Extracting Function Definitions and Calls
- **Approach**: AST traversal via cursors
- **Function Definitions**:
  ```python
  if node.kind == CursorKind.FUNCTION_DECL:
      function_name = node.spelling
  ```
- **Function Calls**:
  ```python
  if node.kind == CursorKind.CALL_EXPR:
      called_function = node.spelling
  ```
- **Traversal Pattern**:
  ```python
  def traverse(node):
      for child in node.get_children():
          traverse(child)
  ```
- **Learning Curve**: Low-moderate - straightforward Python API
- **AST Type**: True Abstract Syntax Tree with semantic information
- **Ease Rating**: 8/10 - Well-documented pattern, many examples available

### Known Limitations
1. **Documentation**: Python bindings lack comprehensive documentation (source code + examples only)
2. **Unexposed Statements**: Some AST nodes exposed as "unexposed statements" without specific kind information
3. **High-level Indexing**: Not implemented in Python bindings
4. **Translation Unit Load Failures**: Don't expose details about why loading failed
5. **Windows Issues**: Occasional access violation errors in `get_children()` (outstanding bugs)
6. **Include Paths**: Requires correct include paths for complete parsing
7. **Performance**: Can be slow without proper configuration
8. **Header Dependencies**: AST includes all dependencies from headers, which can create large ASTs

### Use Case Fit
- **Best For**: Semantic analysis, type resolution, compiler-like tooling, refactoring tools
- **Excellent For**: Dependency analysis with full type information
- **Dependency Analysis**: Ideal - can resolve overloads, templates, virtual functions, and provide semantic context

---

## 3. pycparser

### Maintenance Status
- **Last Release**: 2.23 (September 9, 2025)
- **Previous Release**: 2.22 (March 30, 2024)
- **Activity**: Actively maintained, regular updates
- **Scope**: C99 language only, by design

### C++ Version Support
- **C++11**: ❌ Not supported
- **C++17**: ❌ Not supported
- **C++20**: ❌ Not supported
- **C Language**: ✅ Full C99 support (ISO/IEC 9899)
- **Design Philosophy**: Deliberately C-only to maintain simplicity and maintainability
- **Official Stance**: "For C++, use Clang with Python bindings"

### Installation & Dependencies
```bash
pip install pycparser
```

**Dependencies**: PLY (Python Lex-Yacc) parsing library
**Platform Support**: Pure Python, works on all platforms
**Cross-platform**: ✅ Excellent (pure Python)

### Performance Characteristics
- Not applicable for C++ parsing

### Ease of Extracting Function Definitions and Calls
- Not applicable for C++ code

### Known Limitations
1. **No C++ Support**: Fundamental limitation - only parses C99
2. **No Compiler Extensions**: Doesn't support compiler-specific extensions
3. **Not Suitable**: Explicitly not recommended for C++ parsing

### Use Case Fit
- **For C++ Projects**: ❌ Unsuitable - Cannot parse C++ syntax at all
- **Recommendation**: Disqualified from consideration for C++ dependency analysis

---

## 4. CppHeaderParser / cxxheaderparser

### Maintenance Status

**Original CppHeaderParser**:
- Author: Jashua Cloutier
- Version: 2.7.4
- Status: Maintainer appears busy, limited maintenance
- PyPI: Still available but not actively developed

**robotpy-cppheaderparser (Fork)**:
- Status: DEPRECATED as of 2024
- Last Release: 5.1.2 (May 28, 2024)
- Recommendation: Migrate to cxxheaderparser

**cxxheaderparser (Complete Rewrite - Current)**:
- **Last Release**: 1.6.0 (September 6, 2025)
- **Activity**: Very active with multiple 2024-2025 releases
- **Recent Releases**:
  - 2025: 1.6.0 (Sep), 1.4.1 (Mar)
  - 2024: 1.4.1 (Oct), 1.4.0 (Sep), 1.3.4 (Aug), 1.3.3 (Jun), 1.3.2 (May), 1.3.1 (Jan)
- **Maintenance**: Excellent - regular updates and improvements

### C++ Version Support
- **C++11**: ✅ Good support for modern features
- **C++17**: ⚠️ Partial support - "not all C++17 constructs are supported yet"
- **C++20**: ⚠️ Partial support - "not all C++20 constructs are supported yet"
- **Contributions Welcome**: Open to community PRs for missing features
- **Known Issues**: "Will struggle with obscure or overly complex things"

### Installation & Dependencies
```bash
pip install cxxheaderparser
```

**Dependencies**: dataclasses (minimal)
**Package Type**: Pure Python wheel (py3-none-any)
**Platform Support**: Universal - works on all platforms
**Cross-platform**: ✅ Excellent (pure Python)

### Performance Characteristics
- **Speed**: Not benchmarked in available sources
- **Expected**: Moderate (pure Python implementation)
- **Optimization**: Limited (no native code compilation)
- **10k Line Files**: Likely 1-10 seconds (estimated, no hard data)

### Ease of Extracting Function Definitions and Calls
- **Approach**: Header-focused parsing (not full source files)
- **Scope**: Designed primarily for header files, not implementation files
- **API**: Python-native data structures
- **Learning Curve**: Low - straightforward Python API
- **Documentation**: Available at readthedocs.io
- **Ease Rating**: 7/10 - Simple API but limited to headers

### Known Limitations
1. **Header Files Only**: Designed for parsing header files, may struggle with .cpp implementation files
2. **Incomplete C++17/20 Support**: Explicitly acknowledges gaps in modern C++ support
3. **Complex Constructs**: Will struggle with obscure or overly complex code
4. **Function Calls**: Not designed to extract function calls from implementation files
5. **Semantic Analysis**: Limited compared to compiler-based tools
6. **Pure Python Performance**: Slower than compiled alternatives

### Use Case Fit
- **Best For**: Parsing C++ header files for interface extraction, binding generation
- **Not Ideal For**: Full source code analysis, implementation file parsing
- **Dependency Analysis**: Limited - primarily header-focused, missing implementation analysis
- **Recommendation**: Not suitable for analyzing function calls across implementation files

---

## Comparative Summary Table

| Feature | tree-sitter-cpp | libclang | pycparser | cxxheaderparser |
|---------|----------------|----------|-----------|----------------|
| **C++17 Support** | ⚠️ Partial | ✅ Full | ❌ N/A | ⚠️ Partial |
| **C++20 Support** | ⚠️ Limited | ✅ Most | ❌ N/A | ⚠️ Partial |
| **Maintenance (2024-2025)** | ✅ Active | ✅ Active | ✅ Active (C-only) | ✅ Very Active |
| **Cross-Platform** | ✅ Excellent | ✅ Excellent | ✅ Excellent | ✅ Excellent |
| **Pip Installable** | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **External Dependencies** | None (wheels) | None (bundled) | PLY | dataclasses |
| **AST Quality** | CST only | True AST | AST (C99) | Header-focused |
| **Performance (10k lines)** | <50ms | 1-5s | N/A | 1-10s (est.) |
| **Function Definitions** | ✅ Good | ✅ Excellent | ❌ N/A | ⚠️ Headers only |
| **Function Calls** | ✅ Syntax only | ✅ Full semantic | ❌ N/A | ❌ Limited |
| **Semantic Analysis** | ❌ No | ✅ Yes | ❌ N/A | ⚠️ Limited |
| **Template Resolution** | ❌ No | ✅ Yes | ❌ N/A | ⚠️ Limited |
| **Learning Curve** | Moderate | Low-Moderate | N/A | Low |
| **Documentation** | Good | Limited | Good | Good |
| **Python Versions** | 3.9+ | 2.7, 3.3-3.12 | 2.7, 3.x | 3.x |
| **Suitability for Dependency Analysis** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐ |

**Legend**: ✅ Excellent, ⚠️ Partial/Limited, ❌ Not Supported, ⭐ Rating out of 5

---

## Detailed Recommendation

### First Choice: libclang (via `libclang` PyPI package)

**Rationale**:
1. **Complete Modern C++ Support**: Full C++17 support and most C++20 features
2. **Semantic Understanding**: True AST with type information, template resolution, overload resolution
3. **Production Ready**: Backed by LLVM, used in production tooling worldwide
4. **Zero External Dependencies**: Bundled library means `pip install libclang` just works
5. **Cross-Platform**: Comprehensive platform support with pre-built wheels
6. **Function Analysis**: Can accurately identify function definitions AND function calls with full semantic context
7. **Dependency Resolution**: Can resolve virtual functions, templates, overloads - critical for accurate dependency analysis

**Trade-offs**:
- Slower than tree-sitter (but adequate for batch processing)
- Requires proper configuration for optimal performance
- Documentation for Python bindings is limited (but many examples available)

**Best For**:
- Building a comprehensive C++ function dependency analyzer
- Need to handle modern C++ codebases (C++17/C++20)
- Require semantic accuracy for dependency graphs
- Willing to trade some performance for correctness

### Second Choice: tree-sitter with tree-sitter-cpp

**When to Consider**:
- Performance is critical (need sub-second parsing)
- Only need syntactic analysis (don't need type resolution)
- Working with simpler C++ code (C++11-era, not heavy template metaprogramming)
- Building real-time tools (editor integration, live analysis)
- Incremental parsing is a requirement

**Not Recommended If**:
- Need to resolve templates, overloads, or virtual functions
- Working with C++20 codebases (modules, concepts)
- Require accurate semantic dependency analysis

### Not Recommended

**pycparser**:
- Only parses C, not C++. Immediately disqualified.

**cxxheaderparser**:
- Header-focused tool, not designed for full source file analysis
- Cannot extract function calls from implementation files
- Incomplete C++17/C++20 support
- Not suitable for comprehensive dependency analysis

---

## Implementation Guidance for libclang

### Basic Setup
```python
from clang.cindex import Index, CursorKind

# Create index
index = Index.create()

# Parse translation unit
tu = index.parse('myfile.cpp', args=['-std=c++17', '-I/path/to/includes'])

# Traverse AST
def traverse(node, depth=0):
    # Check for function definitions
    if node.kind == CursorKind.FUNCTION_DECL:
        print(f"Function: {node.spelling}")

    # Check for function calls
    if node.kind == CursorKind.CALL_EXPR:
        print(f"Calls: {node.spelling}")

    # Recurse
    for child in node.get_children():
        traverse(child, depth + 1)

traverse(tu.cursor)
```

### Performance Optimization
```python
# Use flags for better performance
tu = index.parse(
    'myfile.cpp',
    args=['-std=c++17'],
    options=(
        CXTranslationUnit_SkipFunctionBodies |  # Skip parsing function bodies if not needed
        CXTranslationUnit_SingleFileParse       # Don't parse included files
    )
)

# Use precompiled headers for standard library
# Create PCH: clang++ -x c++-header -std=c++17 stdafx.h -o stdafx.pch
tu = index.parse('myfile.cpp', args=['-std=c++17', '-include-pch', 'stdafx.pch'])
```

### Key Considerations
1. **Include Paths**: Always provide correct `-I` flags for includes
2. **Standard Version**: Specify `-std=c++17` or `-std=c++20` as needed
3. **Precompiled Headers**: Use for standard library to improve performance
4. **Translation Units**: Parse each .cpp file separately (C++ compilation model)
5. **Error Handling**: Check `tu.diagnostics` for parsing errors

---

## Conclusion

For building a C++ function dependency analyzer that handles modern C++17/C++20 code, **libclang** is the clear winner. Its comprehensive language support, semantic analysis capabilities, and mature ecosystem outweigh its moderate performance overhead. The tool's ability to accurately resolve templates, overloads, and virtual functions is essential for producing accurate dependency graphs.

While tree-sitter offers impressive performance, its syntactic-only parsing and incomplete C++17/C++20 support make it unsuitable for semantic dependency analysis. The other options (pycparser and cxxheaderparser) are not designed for comprehensive C++ source analysis and should not be considered for this use case.

**Final Recommendation**: Use `libclang` (version 18.1.1 or later) installed via `pip install libclang`.
