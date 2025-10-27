"""Integration tests for end-to-end analysis workflows."""

from pathlib import Path

import pytest

from function_grouper.analyzer.call_analyzer import CallAnalyzer
from function_grouper.analyzer.grouper import Grouper
from function_grouper.parser.cpp_parser import CppParser


@pytest.mark.integration
class TestEndToEnd:
    """End-to-end integration tests."""

    def test_simple_independent_cpp(self, simple_independent_cpp: Path) -> None:
        """Test complete workflow with simple_independent.cpp fixture.

        Expected: 3 independent groups (one per function).
        """
        # Parse the file
        parser = CppParser()
        functions = parser.parse_file(str(simple_independent_cpp))

        # Should find 3 functions
        assert len(functions) == 3

        # Build call graph
        analyzer = CallAnalyzer()
        call_graph = analyzer.build_call_graph(functions)

        # Should have 3 functions in graph
        assert len(call_graph) == 3

        # Find groups
        grouper = Grouper()
        groups = grouper.find_independent_groups(call_graph)

        # Should have 3 groups
        assert len(groups) == 3

        # All groups should be independent
        assert all(g.is_independent for g in groups)

        # Each group should have 1 function
        assert all(len(g) == 1 for g in groups)

        # No internal edges (no function calls)
        assert all(g.internal_edges == 0 for g in groups)

    def test_complex_dependencies_cpp(self, complex_dependencies_cpp: Path) -> None:
        """Test complete workflow with complex_dependencies.cpp fixture.

        Expected: 2 groups
        - Group 1: helper, process, analyze (connected)
        - Group 2: independentFunction (isolated)
        """
        # Parse the file
        parser = CppParser()
        functions = parser.parse_file(str(complex_dependencies_cpp))

        # Should find 4 functions
        assert len(functions) == 4

        # Build call graph
        analyzer = CallAnalyzer()
        call_graph = analyzer.build_call_graph(functions)

        # Should have 4 functions in graph
        assert len(call_graph) == 4

        # Find groups
        grouper = Grouper()
        groups = grouper.find_independent_groups(call_graph)

        # Should have 2 groups
        assert len(groups) == 2

        # Find the sizes
        group_sizes = sorted([len(g) for g in groups])
        assert group_sizes == [1, 3]

        # The group of size 1 should be independent
        single_func_group = next(g for g in groups if len(g) == 1)
        assert single_func_group.is_independent

        # The group of size 3 should have internal edges
        multi_func_group = next(g for g in groups if len(g) == 3)
        assert multi_func_group.internal_edges > 0

    def test_circular_deps_cpp(self, circular_deps_cpp: Path) -> None:
        """Test complete workflow with circular_deps.cpp fixture.

        Expected: 1 group with circular dependency.
        """
        # Parse the file
        parser = CppParser()
        functions = parser.parse_file(str(circular_deps_cpp))

        # Should find 2 functions
        assert len(functions) == 2

        # Build call graph
        analyzer = CallAnalyzer()
        call_graph = analyzer.build_call_graph(functions)

        # Should have 2 functions in graph
        assert len(call_graph) == 2

        # Graph should have a cycle
        assert call_graph.has_cycle()

        # Find groups
        grouper = Grouper()
        groups = grouper.find_independent_groups(call_graph)

        # Should have 1 group
        assert len(groups) == 1

        # Group should contain both functions
        assert len(groups[0]) == 2

        # Group should have cycles
        assert groups[0].has_cycles is True

    def test_empty_file_returns_empty_results(self, temp_cpp_file: Path) -> None:
        """Test that an empty file returns empty results."""
        temp_cpp_file.write_text("")

        parser = CppParser()
        functions = parser.parse_file(str(temp_cpp_file))

        assert len(functions) == 0

        analyzer = CallAnalyzer()
        call_graph = analyzer.build_call_graph(functions)

        assert len(call_graph) == 0

        grouper = Grouper()
        groups = grouper.find_independent_groups(call_graph)

        assert len(groups) == 0
