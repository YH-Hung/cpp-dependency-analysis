"""Contract tests for output format compliance.

Tests that JSON and DOT outputs conform to their published schemas/formats.
"""

import json
import subprocess
from pathlib import Path

import pytest
from jsonschema import validate
from jsonschema.exceptions import ValidationError


@pytest.fixture
def json_schema():
    """Load the JSON output schema from contracts."""
    schema_path = Path(__file__).parent.parent.parent / "specs" / "001-function-grouper" / "contracts" / "json-output-schema.json"
    with open(schema_path) as f:
        return json.load(f)


@pytest.fixture
def simple_cpp_file(tmp_path):
    """Create a simple C++ test file."""
    cpp_file = tmp_path / "simple.cpp"
    cpp_file.write_text("""
void independent1() {
    // standalone function
}

void independent2() {
    // another standalone function
}

void caller() {
    independent1();
}
""")
    return cpp_file


class TestJSONSchemaCompliance:
    """Test JSON output compliance with published schema (T061)."""

    def test_json_output_validates_against_schema(self, json_schema, simple_cpp_file):
        """JSON output must validate against json-output-schema.json."""
        # Run the tool with JSON output
        result = subprocess.run(
            ["python", "-m", "function_grouper", "-f", "json", str(simple_cpp_file)],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"Tool failed: {result.stderr}"

        # Parse JSON output
        output_data = json.loads(result.stdout)

        # Validate against schema
        try:
            validate(instance=output_data, schema=json_schema)
        except ValidationError as e:
            pytest.fail(f"JSON output does not conform to schema: {e.message}")

    def test_json_has_required_metadata_fields(self, simple_cpp_file):
        """JSON output must include all required metadata fields."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", "-f", "json", str(simple_cpp_file)],
            capture_output=True,
            text=True,
            check=True,
        )

        output_data = json.loads(result.stdout)
        metadata = output_data["metadata"]

        required_fields = [
            "source_file",
            "parse_timestamp",
            "total_functions",
            "successfully_parsed",
            "failed_to_parse",
            "total_call_edges",
            "total_groups",
            "independent_groups",
            "largest_group_size",
            "analysis_duration_seconds",
            "memory_used_mb",
        ]

        for field in required_fields:
            assert field in metadata, f"Missing required metadata field: {field}"

    def test_json_metadata_types(self, simple_cpp_file):
        """Metadata fields must have correct types."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", "-f", "json", str(simple_cpp_file)],
            capture_output=True,
            text=True,
            check=True,
        )

        output_data = json.loads(result.stdout)
        metadata = output_data["metadata"]

        # String fields
        assert isinstance(metadata["source_file"], str)
        assert isinstance(metadata["parse_timestamp"], str)

        # Integer fields
        assert isinstance(metadata["total_functions"], int)
        assert isinstance(metadata["successfully_parsed"], int)
        assert isinstance(metadata["failed_to_parse"], int)
        assert isinstance(metadata["total_call_edges"], int)
        assert isinstance(metadata["total_groups"], int)
        assert isinstance(metadata["independent_groups"], int)
        assert isinstance(metadata["largest_group_size"], int)

        # Number fields (float or int)
        assert isinstance(metadata["analysis_duration_seconds"], (int, float))
        assert isinstance(metadata["memory_used_mb"], (int, float))

    def test_json_functions_array_structure(self, simple_cpp_file):
        """Functions array must have correct structure."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", "-f", "json", str(simple_cpp_file)],
            capture_output=True,
            text=True,
            check=True,
        )

        output_data = json.loads(result.stdout)
        functions = output_data["functions"]

        assert isinstance(functions, list)

        # Check each function has required fields
        required_fields = ["name", "qualified_name", "signature", "location", "kind", "calls", "parse_status"]
        for func in functions:
            for field in required_fields:
                assert field in func, f"Function missing required field: {field}"

    def test_json_groups_array_structure(self, simple_cpp_file):
        """Groups array must have correct structure."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", "-f", "json", str(simple_cpp_file)],
            capture_output=True,
            text=True,
            check=True,
        )

        output_data = json.loads(result.stdout)
        groups = output_data["groups"]

        assert isinstance(groups, list)
        assert len(groups) > 0, "Should have at least one group"

        # Check each group has required fields
        required_fields = ["group_id", "functions", "is_independent", "internal_edges", "external_edges", "has_cycles"]
        for group in groups:
            for field in required_fields:
                assert field in group, f"Group missing required field: {field}"

            # Type checks
            assert isinstance(group["group_id"], int)
            assert isinstance(group["functions"], list)
            assert isinstance(group["is_independent"], bool)
            assert isinstance(group["internal_edges"], int)
            assert isinstance(group["external_edges"], int)
            assert isinstance(group["has_cycles"], bool)

    def test_json_independent_group_has_zero_external_edges(self, simple_cpp_file):
        """Groups marked as independent must have 0 external edges."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", "-f", "json", str(simple_cpp_file)],
            capture_output=True,
            text=True,
            check=True,
        )

        output_data = json.loads(result.stdout)
        groups = output_data["groups"]

        for group in groups:
            if group["is_independent"]:
                assert group["external_edges"] == 0, (
                    f"Group {group['group_id']} is marked independent but has "
                    f"{group['external_edges']} external edges"
                )


class TestDOTFormatValidity:
    """Test DOT output validity (T062)."""

    def test_dot_output_is_valid_graphviz_syntax(self, simple_cpp_file):
        """DOT output must be parseable by Graphviz."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", "-f", "dot", str(simple_cpp_file)],
            capture_output=True,
            text=True,
            check=True,
        )

        dot_output = result.stdout

        # Basic syntax checks
        assert dot_output.strip().startswith("digraph"), "DOT output must start with 'digraph'"
        assert "{" in dot_output, "DOT output must contain opening brace"
        assert "}" in dot_output, "DOT output must contain closing brace"

        # Try to validate with dot command if available
        dot_check = subprocess.run(
            ["dot", "-Tsvg", "-o", "/dev/null"],
            input=dot_output,
            capture_output=True,
            text=True,
            check=False,
        )

        # If dot is available, it should parse without errors
        if dot_check.returncode != 127:  # 127 = command not found
            assert dot_check.returncode == 0, f"Graphviz dot failed to parse output: {dot_check.stderr}"

    def test_dot_contains_function_nodes(self, simple_cpp_file):
        """DOT output must contain function nodes."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", "-f", "dot", str(simple_cpp_file)],
            capture_output=True,
            text=True,
            check=True,
        )

        dot_output = result.stdout

        # Should contain at least one node definition (quoted string with label or shape)
        assert '"' in dot_output, "DOT output should contain quoted node names"
        # Common node attributes
        assert any(keyword in dot_output for keyword in ["label=", "shape=", "color="]), \
            "DOT output should contain node attributes"

    def test_dot_contains_edges_for_function_calls(self, simple_cpp_file):
        """DOT output must contain edges representing function calls."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", "-f", "dot", str(simple_cpp_file)],
            capture_output=True,
            text=True,
            check=True,
        )

        dot_output = result.stdout

        # Should contain at least one edge (->)
        # The simple.cpp has a call from caller() to independent1()
        assert "->" in dot_output, "DOT output should contain edges (->)"

    def test_dot_contains_cluster_subgraphs(self, simple_cpp_file):
        """DOT output must contain cluster subgraphs for groups."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", "-f", "dot", str(simple_cpp_file)],
            capture_output=True,
            text=True,
            check=True,
        )

        dot_output = result.stdout

        # Should contain cluster subgraphs for grouping
        assert "subgraph cluster" in dot_output, "DOT output should contain cluster subgraphs"

    def test_dot_output_is_utf8_encoded(self, simple_cpp_file):
        """DOT output must be UTF-8 encoded."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", "-f", "dot", str(simple_cpp_file)],
            capture_output=True,
            check=True,
        )

        # Should be decodable as UTF-8
        try:
            result.stdout.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail("DOT output is not valid UTF-8")
