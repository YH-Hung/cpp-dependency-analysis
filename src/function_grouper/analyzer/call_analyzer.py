"""Call graph analysis and construction."""


from function_grouper.models import CallGraph, Function


class CallAnalyzer:
    """Analyzes function calls and builds call graphs."""

    def build_call_graph(self, functions: list[Function]) -> CallGraph:
        """Build a call graph from a list of functions.

        Args:
            functions: List of Function objects

        Returns:
            CallGraph with all functions and their call relationships
        """
        graph = CallGraph()

        # First pass: Add all functions to the graph
        # For overloaded functions, use signature as the unique key
        seen_names = set()
        for func in functions:
            # Use signature as unique identifier for overloaded functions
            unique_name = func.qualified_name
            if unique_name in seen_names:
                # Overloaded function - append signature to make it unique
                unique_name = f"{func.qualified_name}({func.signature.split('(', 1)[1]}"

            seen_names.add(unique_name)

            # Create a modified function with unique qualified_name
            if unique_name != func.qualified_name:
                from dataclasses import replace
                func = replace(func, qualified_name=unique_name)

            graph.add_function(func)

        # Second pass: Add call edges
        for func in functions:
            for callee in func.calls:
                # Only add edges if both caller and callee are in the graph
                if callee in graph:
                    graph.add_call(func.qualified_name, callee, func.location)

        return graph
