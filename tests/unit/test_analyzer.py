"""Unit tests for analyzer module."""

import pytest

from function_grouper.models import (
    CallGraph,
    Function,
    FunctionKind,
    SourceLocation,
)


class TestCallGraph:
    """Test cases for CallGraph class."""

    def test_add_function(self) -> None:
        """Test adding a function to the call graph."""
        graph = CallGraph()
        func = Function(
            name="test",
            qualified_name="test",
            signature="void test()",
            location=SourceLocation("/test.cpp", 1, 1),
            kind=FunctionKind.FREE_FUNCTION,
        )

        graph.add_function(func)

        assert len(graph) == 1
        assert "test" in graph
        assert graph.functions["test"] == func

    def test_add_duplicate_function_raises_error(self) -> None:
        """Test that adding a duplicate function raises an error."""
        graph = CallGraph()
        func = Function(
            name="test",
            qualified_name="test",
            signature="void test()",
            location=SourceLocation("/test.cpp", 1, 1),
            kind=FunctionKind.FREE_FUNCTION,
        )

        graph.add_function(func)

        with pytest.raises(ValueError, match="already exists"):
            graph.add_function(func)

    def test_add_call(self) -> None:
        """Test adding a call edge between functions."""
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

        assert len(graph.edges) == 1
        assert graph.edges[0].caller == "funcA"
        assert graph.edges[0].callee == "funcB"

    def test_add_call_to_nonexistent_function_ignores(self) -> None:
        """Test that calling a function not in the graph is silently ignored (external call)."""
        graph = CallGraph()

        func = Function(
            name="caller",
            qualified_name="caller",
            signature="void caller()",
            location=SourceLocation("/test.cpp", 1, 1),
            kind=FunctionKind.FREE_FUNCTION,
        )

        graph.add_function(func)
        # This should not raise an error (external call)
        graph.add_call("caller", "externalFunc")

        # Should have no edges since externalFunc is not in the graph
        assert len(graph.edges) == 0

    def test_get_callers(self) -> None:
        """Test getting callers of a function."""
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

        callers = graph.get_callers("funcB")
        assert "funcA" in callers

    def test_get_callees(self) -> None:
        """Test getting callees of a function."""
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

        callees = graph.get_callees("funcA")
        assert "funcB" in callees

    def test_has_cycle_detects_circular_dependencies(self) -> None:
        """Test detecting circular dependencies."""
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

        assert graph.has_cycle() is True

    def test_has_cycle_returns_false_for_acyclic_graph(self) -> None:
        """Test that acyclic graphs return False for has_cycle."""
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

        assert graph.has_cycle() is False
