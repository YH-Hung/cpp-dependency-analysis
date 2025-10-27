"""Unit tests for C++ parser module."""

from pathlib import Path

import pytest

from function_grouper.models import Function, FunctionKind, ParseStatus
from function_grouper.parser.cpp_parser import CppParser


class TestCppParser:
    """Test cases for CppParser class."""

    def test_parse_file_with_simple_function(self, temp_cpp_file: Path) -> None:
        """Test parsing a simple free function."""
        temp_cpp_file.write_text("""
void hello() {
    // Empty function
}
""")
        parser = CppParser()
        functions = parser.parse_file(str(temp_cpp_file))

        assert len(functions) == 1
        assert functions[0].name == "hello"
        assert functions[0].kind == FunctionKind.FREE_FUNCTION
        assert functions[0].parse_status == ParseStatus.SUCCESS

    def test_parse_file_extracts_function_names_and_signatures(self, temp_cpp_file: Path) -> None:
        """Test extracting function names and signatures correctly."""
        temp_cpp_file.write_text("""
int add(int a, int b) {
    return a + b;
}

double multiply(double x, double y) {
    return x * y;
}
""")
        parser = CppParser()
        functions = parser.parse_file(str(temp_cpp_file))

        assert len(functions) == 2

        # Check first function
        add_func = next(f for f in functions if f.name == "add")
        assert "int" in add_func.signature
        assert "add" in add_func.signature

        # Check second function
        mult_func = next(f for f in functions if f.name == "multiply")
        assert "double" in mult_func.signature
        assert "multiply" in mult_func.signature

    def test_parse_file_identifies_function_calls(self, temp_cpp_file: Path) -> None:
        """Test identifying function calls within function bodies."""
        temp_cpp_file.write_text("""
void helper() {
    int x = 0;
}

void caller() {
    helper();
}
""")
        parser = CppParser()
        functions = parser.parse_file(str(temp_cpp_file))

        assert len(functions) == 2

        # Find the caller function
        caller_func = next(f for f in functions if f.name == "caller")
        assert len(caller_func.calls) >= 1
        # Should call helper
        assert any("helper" in call for call in caller_func.calls)

    def test_parse_file_handles_member_functions(self, temp_cpp_file: Path) -> None:
        """Test parsing member functions (methods)."""
        temp_cpp_file.write_text("""
class MyClass {
public:
    void method() {
        // Member function
    }
};
""")
        parser = CppParser()
        functions = parser.parse_file(str(temp_cpp_file))

        # Should find the member function
        assert len(functions) >= 1
        method_func = next((f for f in functions if "method" in f.name), None)
        assert method_func is not None

    def test_parse_file_with_multiple_functions(self, temp_cpp_file: Path) -> None:
        """Test parsing file with multiple functions."""
        temp_cpp_file.write_text("""
void func1() {}
void func2() {}
void func3() {}
""")
        parser = CppParser()
        functions = parser.parse_file(str(temp_cpp_file))

        assert len(functions) == 3
        names = [f.name for f in functions]
        assert "func1" in names
        assert "func2" in names
        assert "func3" in names

    def test_parse_file_handles_empty_file(self, temp_cpp_file: Path) -> None:
        """Test parsing an empty file."""
        temp_cpp_file.write_text("")
        parser = CppParser()
        functions = parser.parse_file(str(temp_cpp_file))

        assert len(functions) == 0

    def test_parse_file_with_invalid_path_raises_error(self) -> None:
        """Test that parsing non-existent file raises appropriate error."""
        parser = CppParser()
        with pytest.raises(Exception):  # Should raise FileNotFoundError or similar
            parser.parse_file("/nonexistent/path/to/file.cpp")
