# C++ Function Grouper

Analyze C++ function dependencies and identify independent groups.

## Overview

The C++ Function Grouper is a command-line tool that analyzes C++ implementation files to identify independent function groups based on call relationships. It uses AST-based parsing (libclang) to build dependency graphs and performs connected component analysis to find functions that do not reference each other.

## Features

- **AST-based parsing**: Uses libclang for accurate C++17/C++20 parsing
- **Dependency analysis**: Builds call graphs showing function relationships
- **Group detection**: Identifies independent function groups using connected components
- **Multiple output formats**: JSON, plain text, and Graphviz DOT
- **Performance**: Handles 10,000-line files with up to 1000 functions
- **Graceful error handling**: Continues with partial analysis on parse errors

## Installation

### Requirements

- Python 3.11 or later
- libclang 18.1.1 or later

### Install from source

```bash
# Clone the repository
git clone <repository-url>
cd cpp-dependency-analysis

# Install with pip
pip install -e ".[dev]"
```

## Usage

### Basic Usage

```bash
# Analyze a C++ file with default text output
function-grouper my_code.cpp

# Save JSON output
function-grouper -f json -o results.json my_code.cpp

# Use C++20 standard
function-grouper --std c++20 modern_code.cpp
```

### Output Formats

- **Text** (default): Human-readable summary with group information
- **JSON**: Structured data with full metadata
- **DOT**: Graphviz format for visualization

### Advanced Options

```bash
# Add include paths
function-grouper -I ./include -I ../common/headers file.cpp

# Generate Graphviz visualization
function-grouper -f dot -o graph.dot file.cpp
dot -Tpng graph.dot -o graph.png

# Strict mode (fail on any parse error)
function-grouper --strict --verbose file.cpp
```

## Example Output

Given a C++ file with function dependencies:

```cpp
void helper() {
    int temp = 0;
}

void process() {
    helper();
}

void independentFunction() {
    double value = 42.0;
}
```

The tool identifies:
- **Group 1**: `helper`, `process` (connected via function call)
- **Group 2**: `independentFunction` (independent)

## Development

### Setup Development Environment

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run linter
ruff check src/ tests/

# Run type checker
mypy src/function_grouper

# Run tests with coverage
pytest --cov=src/function_grouper --cov-report=html
```

### Project Structure

```
cpp-dependency-analysis/
├── src/function_grouper/    # Main package
│   ├── parser/              # C++ AST parsing
│   ├── analyzer/            # Call graph and grouping
│   ├── formatter/           # Output formatters
│   ├── cli/                 # Command-line interface
│   └── models/              # Data models
└── tests/                   # Test suite
    ├── unit/                # Unit tests
    ├── integration/         # Integration tests
    └── contract/            # Contract tests
```

## Success Criteria

- Parse 10,000-line files in under 30 seconds
- Handle up to 1000 function definitions
- Memory usage under 2GB
- 100% accuracy on files with known dependencies
- 95%+ parse success rate on real-world C++ code

## License

See LICENSE file for details.

## Contributing

Contributions are welcome! Please see CONTRIBUTING.md for guidelines.
