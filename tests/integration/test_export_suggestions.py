"""Integration tests for export suggestions feature (User Story 3).

Tests the end-to-end functionality of suggesting file splits based on
independent function groups.
"""

import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def cpp_file_with_independent_groups(tmp_path):
    """Create a C++ file with clear independent groups for testing."""
    cpp_file = tmp_path / "modules.cpp"
    cpp_file.write_text("""
// Group 1: Math utilities (independent)
int add(int a, int b) {
    return a + b;
}

int multiply(int a, int b) {
    return a * b;
}

int calculate_sum(int x, int y) {
    return add(x, y);
}

// Group 2: String utilities (independent)
void print_string(const char* str) {
    // print implementation
}

void format_string(const char* input) {
    print_string(input);
}

// Group 3: Main logic (depends on Group 1)
int process_values(int a, int b) {
    int sum = add(a, b);
    int product = multiply(a, b);
    return sum + product;
}
""")
    return cpp_file


def test_export_suggestions_with_json_output(cpp_file_with_independent_groups):
    """Test that --export-suggestions works with JSON output."""
    result = subprocess.run(
        [
            "python", "-m", "function_grouper",
            "--export-suggestions",
            "-f", "json",
            str(cpp_file_with_independent_groups)
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    # Parse JSON output
    import json
    output = json.loads(result.stdout)

    # Should have export_suggestions field
    assert "export_suggestions" in output, "JSON should contain export_suggestions when flag is used"
    assert isinstance(output["export_suggestions"], list), "export_suggestions should be a list"


def test_export_suggestions_with_text_output(cpp_file_with_independent_groups):
    """Test that --export-suggestions works with text output."""
    result = subprocess.run(
        [
            "python", "-m", "function_grouper",
            "--export-suggestions",
            "-f", "text",
            str(cpp_file_with_independent_groups)
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    output = result.stdout.lower()

    # Text output should mention suggestions or recommended splits
    assert any(keyword in output for keyword in ["suggest", "recommend", "split", "export"]), \
        "Text output should mention export suggestions"


def test_export_suggestions_identifies_independent_groups(cpp_file_with_independent_groups):
    """Test that export suggestions correctly identify independent groups."""
    result = subprocess.run(
        [
            "python", "-m", "function_grouper",
            "--export-suggestions",
            "-f", "json",
            str(cpp_file_with_independent_groups)
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    import json
    output = json.loads(result.stdout)

    # Should have multiple groups
    groups = output["groups"]
    assert len(groups) >= 2, "Should identify multiple function groups"

    # Should have some independent groups
    independent_groups = [g for g in groups if g["is_independent"]]
    assert len(independent_groups) >= 1, "Should have at least one independent group"

    # Export suggestions should reference independent groups
    if output.get("export_suggestions"):
        suggestions = output["export_suggestions"]
        assert len(suggestions) > 0, "Should provide export suggestions"


def test_without_export_suggestions_flag(cpp_file_with_independent_groups):
    """Test that suggestions are NOT included without --export-suggestions flag."""
    result = subprocess.run(
        [
            "python", "-m", "function_grouper",
            "-f", "json",
            str(cpp_file_with_independent_groups)
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    import json
    output = json.loads(result.stdout)

    # Should not have export_suggestions field when flag is not used
    assert "export_suggestions" not in output or output.get("export_suggestions") is None, \
        "Should not include export_suggestions without flag"


def test_export_suggestions_end_to_end_workflow(cpp_file_with_independent_groups, tmp_path):
    """Test complete workflow: parse, analyze, suggest, output to file."""
    output_file = tmp_path / "analysis_with_suggestions.json"

    result = subprocess.run(
        [
            "python", "-m", "function_grouper",
            "--export-suggestions",
            "-f", "json",
            "-o", str(output_file),
            str(cpp_file_with_independent_groups)
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    assert result.returncode == 0, "Command should succeed"
    assert output_file.exists(), "Output file should be created"

    # Verify file content
    import json
    with open(output_file) as f:
        output = json.load(f)

    assert "metadata" in output
    assert "functions" in output
    assert "groups" in output
    assert "export_suggestions" in output


def test_export_suggestions_with_single_independent_function(tmp_path):
    """Test suggestions for a file with only independent functions."""
    cpp_file = tmp_path / "independent_only.cpp"
    cpp_file.write_text("""
void func1() {
    // standalone
}

void func2() {
    // standalone
}

void func3() {
    // standalone
}
""")

    result = subprocess.run(
        [
            "python", "-m", "function_grouper",
            "--export-suggestions",
            "-f", "json",
            str(cpp_file)
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    import json
    output = json.loads(result.stdout)

    # All groups should be independent
    groups = output["groups"]
    assert all(g["is_independent"] for g in groups), \
        "All groups should be independent when no dependencies exist"


def test_export_suggestions_with_circular_dependencies(tmp_path):
    """Test suggestions for a file with circular dependencies."""
    cpp_file = tmp_path / "circular.cpp"
    cpp_file.write_text("""
void funcA();
void funcB();

void funcA() {
    funcB();
}

void funcB() {
    funcA();
}

void independent() {
    // standalone
}
""")

    result = subprocess.run(
        [
            "python", "-m", "function_grouper",
            "--export-suggestions",
            "-f", "json",
            str(cpp_file)
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    import json
    output = json.loads(result.stdout)

    # Should identify circular dependency
    groups = output["groups"]
    circular_groups = [g for g in groups if g["has_cycles"]]

    # At least one group should have cycles (funcA and funcB)
    assert len(circular_groups) > 0, "Should identify circular dependencies"

    # Should still provide export suggestions
    assert "export_suggestions" in output
