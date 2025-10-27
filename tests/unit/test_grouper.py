"""Unit tests for grouper module."""

from function_grouper.analyzer.grouper import Grouper
from function_grouper.models import (
    CallGraph,
    Function,
    FunctionKind,
    SourceLocation,
)


class TestGrouper:
    """Test cases for Grouper class."""

    def test_find_connected_components_with_independent_functions(self) -> None:
        """Test finding groups with independent functions."""
        graph = CallGraph()

        # Create three independent functions
        for i in range(3):
            func = Function(
                name=f"func{i}",
                qualified_name=f"func{i}",
                signature=f"void func{i}()",
                location=SourceLocation("/test.cpp", i + 1, 1),
                kind=FunctionKind.FREE_FUNCTION,
            )
            graph.add_function(func)

        grouper = Grouper()
        groups = grouper.find_independent_groups(graph)

        # Should have 3 groups (each function is independent)
        assert len(groups) == 3
        # All groups should be independent
        assert all(g.is_independent for g in groups)
        # Each group should have 1 function
        assert all(len(g.functions) == 1 for g in groups)

    def test_find_connected_components_with_connected_functions(self) -> None:
        """Test finding groups with connected functions."""
        graph = CallGraph()

        # Create two connected functions
        func_a = Function(
            name="funcA",
            qualified_name="funcA",
            signature="void funcA()",
            location=SourceLocation("/test.cpp", 1, 1),
            kind=FunctionKind.FREE_FUNCTION,
        )

        func_b = Function(
            name="funcB",
            qualified_name="funcB",
            signature="void funcB()",
            location=SourceLocation("/test.cpp", 5, 1),
            kind=FunctionKind.FREE_FUNCTION,
        )

        graph.add_function(func_a)
        graph.add_function(func_b)
        graph.add_call("funcA", "funcB")

        grouper = Grouper()
        groups = grouper.find_independent_groups(graph)

        # Should have 1 group containing both functions
        assert len(groups) == 1
        assert len(groups[0].functions) == 2
        assert "funcA" in groups[0].functions
        assert "funcB" in groups[0].functions

    def test_find_connected_components_mixed_groups(self) -> None:
        """Test finding groups with mix of independent and connected functions."""
        graph = CallGraph()

        # Create connected pair
        func_a = Function(
            name="funcA",
            qualified_name="funcA",
            signature="void funcA()",
            location=SourceLocation("/test.cpp", 1, 1),
            kind=FunctionKind.FREE_FUNCTION,
        )

        func_b = Function(
            name="funcB",
            qualified_name="funcB",
            signature="void funcB()",
            location=SourceLocation("/test.cpp", 5, 1),
            kind=FunctionKind.FREE_FUNCTION,
        )

        # Create independent function
        func_c = Function(
            name="funcC",
            qualified_name="funcC",
            signature="void funcC()",
            location=SourceLocation("/test.cpp", 10, 1),
            kind=FunctionKind.FREE_FUNCTION,
        )

        graph.add_function(func_a)
        graph.add_function(func_b)
        graph.add_function(func_c)
        graph.add_call("funcA", "funcB")

        grouper = Grouper()
        groups = grouper.find_independent_groups(graph)

        # Should have 2 groups
        assert len(groups) == 2

        # Find the group sizes
        group_sizes = sorted([len(g.functions) for g in groups])
        assert group_sizes == [1, 2]

    def test_detect_cycles_in_group(self) -> None:
        """Test detecting cycles within a group."""
        graph = CallGraph()

        func_a = Function(
            name="funcA",
            qualified_name="funcA",
            signature="void funcA()",
            location=SourceLocation("/test.cpp", 1, 1),
            kind=FunctionKind.FREE_FUNCTION,
        )

        func_b = Function(
            name="funcB",
            qualified_name="funcB",
            signature="void funcB()",
            location=SourceLocation("/test.cpp", 5, 1),
            kind=FunctionKind.FREE_FUNCTION,
        )

        graph.add_function(func_a)
        graph.add_function(func_b)
        graph.add_call("funcA", "funcB")
        graph.add_call("funcB", "funcA")  # Creates cycle

        grouper = Grouper()
        groups = grouper.find_independent_groups(graph)

        # Should have 1 group with a cycle
        assert len(groups) == 1
        assert groups[0].has_cycles is True
