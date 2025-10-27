"""Call graph analysis and construction."""

from typing import List

from function_grouper.models import CallGraph, Function


class CallAnalyzer:
    """Analyzes function calls and builds call graphs."""

    def build_call_graph(self, functions: List[Function]) -> CallGraph:
        """Build a call graph from a list of functions.

        Args:
            functions: List of Function objects

        Returns:
            CallGraph with all functions and their call relationships
        """
        graph = CallGraph()

        # First pass: Add all functions to the graph
        for func in functions:
            graph.add_function(func)

        # Second pass: Add call edges
        for func in functions:
            for callee in func.calls:
                # Only add edges if both caller and callee are in the graph
                if callee in graph:
                    graph.add_call(func.qualified_name, callee, func.location)

        return graph
