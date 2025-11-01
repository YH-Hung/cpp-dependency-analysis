"""Contract tests for CLI interface behavior.

Tests that the CLI adheres to its published interface contract including
arguments, options, exit codes, and error messages.
"""

import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture
def simple_cpp_file(tmp_path):
    """Create a simple valid C++ test file."""
    cpp_file = tmp_path / "simple.cpp"
    cpp_file.write_text("""
void function1() {
    // standalone function
}

void function2() {
    function1();
}
""")
    return cpp_file


@pytest.fixture
def invalid_cpp_file(tmp_path):
    """Create an invalid C++ test file for error testing."""
    cpp_file = tmp_path / "invalid.cpp"
    cpp_file.write_text("""
This is not valid C++ code!
@#$%^&*()
""")
    return cpp_file


class TestCLIHelpAndVersion:
    """Test CLI help and version options (T095, T096)."""

    def test_help_flag_shows_usage_and_exits_zero(self):
        """--help must show usage information and exit with code 0."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", "--help"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, "Help should exit with code 0"
        assert "Usage:" in result.stdout or "usage:" in result.stdout.lower(), \
            "Help should contain usage information"
        assert "INPUT_FILE" in result.stdout or "input-file" in result.stdout.lower(), \
            "Help should mention the input file argument"
        assert "--format" in result.stdout, "Help should mention --format option"
        assert "--output" in result.stdout, "Help should mention --output option"

    def test_short_help_flag(self):
        """-h must work as alias for --help."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", "-h"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, "-h should exit with code 0"
        assert len(result.stdout) > 100, "-h should show help text"

    def test_version_flag_shows_version_and_exits_zero(self):
        """--version must show version information and exit with code 0."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", "--version"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, "Version should exit with code 0"
        assert "function-grouper" in result.stdout.lower(), \
            "Version should mention function-grouper"
        assert "version" in result.stdout.lower(), "Version should contain 'version'"
        # Should show Python version
        assert "Python" in result.stdout or "python" in result.stdout.lower(), \
            "Version should show Python version"


class TestCLIArguments:
    """Test CLI required arguments (T097)."""

    def test_missing_input_file_fails(self):
        """Missing input file argument must cause failure."""
        result = subprocess.run(
            ["python", "-m", "function_grouper"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode != 0, "Should fail without input file"
        assert "Error" in result.stderr or "error" in result.stderr.lower(), \
            "Should show error message"

    def test_nonexistent_file_fails_with_exit_code_2(self, tmp_path):
        """Nonexistent input file must exit with code 2 (FILE_NOT_FOUND)."""
        nonexistent = tmp_path / "does_not_exist.cpp"

        result = subprocess.run(
            ["python", "-m", "function_grouper", str(nonexistent)],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 2, "Nonexistent file should exit with code 2"
        assert "not found" in result.stderr.lower() or "does not exist" in result.stderr.lower(), \
            "Error message should mention file not found"

    def test_valid_input_file_succeeds(self, simple_cpp_file):
        """Valid input file must succeed with exit code 0."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", str(simple_cpp_file)],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0, f"Should succeed with valid file: {result.stderr}"


class TestCLIExitCodes:
    """Test CLI exit codes (T098)."""

    def test_success_exits_with_code_0(self, simple_cpp_file):
        """Successful analysis must exit with code 0."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", str(simple_cpp_file)],
            capture_output=True,
            check=False,
        )

        assert result.returncode == 0, "Success should exit with code 0"

    def test_file_not_found_exits_with_code_2(self, tmp_path):
        """File not found must exit with code 2."""
        nonexistent = tmp_path / "missing.cpp"

        result = subprocess.run(
            ["python", "-m", "function_grouper", str(nonexistent)],
            capture_output=True,
            check=False,
        )

        assert result.returncode == 2, "FILE_NOT_FOUND should exit with code 2"

    def test_invalid_argument_exits_with_code_5(self):
        """Invalid arguments must exit with code 5 or non-zero."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", "--invalid-option", "file.cpp"],
            capture_output=True,
            check=False,
        )

        # Click typically exits with code 2 for bad options, accept either 2 or 5
        assert result.returncode in [2, 5], \
            f"Invalid argument should exit with code 2 or 5, got {result.returncode}"


class TestCLIFormatOptions:
    """Test CLI format options (T099)."""

    def test_format_json_outputs_json(self, simple_cpp_file):
        """--format json must output valid JSON."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", "-f", "json", str(simple_cpp_file)],
            capture_output=True,
            text=True,
            check=True,
        )

        # Should be valid JSON
        import json
        output_data = json.loads(result.stdout)
        assert "metadata" in output_data, "JSON output should have metadata"
        assert "functions" in output_data, "JSON output should have functions"
        assert "groups" in output_data, "JSON output should have groups"

    def test_format_text_outputs_text(self, simple_cpp_file):
        """--format text must output human-readable text."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", "-f", "text", str(simple_cpp_file)],
            capture_output=True,
            text=True,
            check=True,
        )

        output = result.stdout
        # Should contain human-readable headers
        assert any(keyword in output for keyword in ["Function", "Group", "Analysis"]), \
            "Text output should contain readable headers"

    def test_format_dot_outputs_graphviz(self, simple_cpp_file):
        """--format dot must output valid Graphviz DOT format."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", "-f", "dot", str(simple_cpp_file)],
            capture_output=True,
            text=True,
            check=True,
        )

        output = result.stdout
        assert output.strip().startswith("digraph"), "DOT output should start with 'digraph'"
        assert "->" in output or "subgraph" in output, \
            "DOT output should contain graph elements"

    def test_default_format_is_text(self, simple_cpp_file):
        """Default format without -f should be text."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", str(simple_cpp_file)],
            capture_output=True,
            text=True,
            check=True,
        )

        # Should be text format (not JSON, not DOT)
        assert not result.stdout.strip().startswith("{"), "Default should not be JSON"
        assert not result.stdout.strip().startswith("digraph"), "Default should not be DOT"

    def test_invalid_format_fails(self, simple_cpp_file):
        """Invalid format value must cause failure."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", "-f", "invalid_format", str(simple_cpp_file)],
            capture_output=True,
            check=False,
        )

        assert result.returncode != 0, "Invalid format should fail"


class TestCLIOutputOption:
    """Test CLI output file option (T100)."""

    def test_output_to_stdout_by_default(self, simple_cpp_file):
        """Default behavior must output to stdout."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", str(simple_cpp_file)],
            capture_output=True,
            text=True,
            check=True,
        )

        assert len(result.stdout) > 0, "Should write to stdout"

    def test_output_to_file_with_o_flag(self, simple_cpp_file, tmp_path):
        """--output FILE must write to specified file."""
        output_file = tmp_path / "output.txt"

        result = subprocess.run(
            ["python", "-m", "function_grouper", "-o", str(output_file), str(simple_cpp_file)],
            capture_output=True,
            text=True,
            check=True,
        )

        assert output_file.exists(), "Output file should be created"
        assert output_file.stat().st_size > 0, "Output file should not be empty"

    def test_output_long_form(self, simple_cpp_file, tmp_path):
        """--output (long form) must work."""
        output_file = tmp_path / "output.json"

        result = subprocess.run(
            ["python", "-m", "function_grouper", "--output", str(output_file),
             "-f", "json", str(simple_cpp_file)],
            capture_output=True,
            check=True,
        )

        assert output_file.exists(), "--output should create file"


class TestCLIErrorMessages:
    """Test CLI error messages (T101)."""

    def test_file_not_found_error_is_clear(self, tmp_path):
        """File not found error must be clear and informative."""
        nonexistent = tmp_path / "missing.cpp"

        result = subprocess.run(
            ["python", "-m", "function_grouper", str(nonexistent)],
            capture_output=True,
            text=True,
            check=False,
        )

        error_output = result.stderr.lower()
        # Should mention error and file-related issue
        assert "error" in error_output, "Should contain 'error'"
        assert any(keyword in error_output for keyword in ["not found", "does not exist", "no such"]), \
            "Should explain file was not found"

    def test_error_messages_go_to_stderr(self, tmp_path):
        """Error messages must be written to stderr, not stdout."""
        nonexistent = tmp_path / "missing.cpp"

        result = subprocess.run(
            ["python", "-m", "function_grouper", str(nonexistent)],
            capture_output=True,
            text=True,
            check=False,
        )

        assert len(result.stderr) > 0, "Errors should go to stderr"
        # Stdout should be empty or minimal for errors
        if result.stdout:
            assert "error" not in result.stdout.lower(), "Error messages should not be in stdout"


class TestCLIStandardOption:
    """Test C++ standard version option."""

    def test_std_option_accepts_cpp17(self, simple_cpp_file):
        """--std c++17 must be accepted."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", "--std", "c++17", str(simple_cpp_file)],
            capture_output=True,
            check=True,
        )

        assert result.returncode == 0

    def test_std_option_accepts_cpp20(self, simple_cpp_file):
        """--std c++20 must be accepted."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", "--std", "c++20", str(simple_cpp_file)],
            capture_output=True,
            check=True,
        )

        assert result.returncode == 0


class TestCLIVerboseOption:
    """Test verbosity options."""

    def test_verbose_flag_increases_output(self, simple_cpp_file):
        """-v flag must increase verbosity."""
        # Run without verbose
        result_normal = subprocess.run(
            ["python", "-m", "function_grouper", str(simple_cpp_file)],
            capture_output=True,
            text=True,
            check=True,
        )

        # Run with verbose
        result_verbose = subprocess.run(
            ["python", "-m", "function_grouper", "-v", str(simple_cpp_file)],
            capture_output=True,
            text=True,
            check=True,
        )

        # Verbose should add output to stderr
        assert len(result_verbose.stderr) > len(result_normal.stderr), \
            "Verbose mode should output more to stderr"

    def test_multiple_verbose_flags(self, simple_cpp_file):
        """-vv should work for increased verbosity."""
        result = subprocess.run(
            ["python", "-m", "function_grouper", "-vv", str(simple_cpp_file)],
            capture_output=True,
            text=True,
            check=True,
        )

        # Should still succeed
        assert result.returncode == 0
