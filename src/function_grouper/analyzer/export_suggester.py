"""Export suggester for recommending file splits based on function groups."""

from typing import Any

from function_grouper.models.call_graph import CallGraph
from function_grouper.models.group import FunctionGroup


class ExportSuggester:
    """Suggests how to split a file based on independent function groups."""

    def suggest_file_splits(
        self, graph: CallGraph, groups: list[FunctionGroup]
    ) -> list[dict[str, Any]]:
        """
        Generate export suggestions for splitting the file.

        Args:
            graph: Call graph containing all functions
            groups: List of function groups

        Returns:
            List of dictionaries with export suggestions for each group
        """
        suggestions = []

        for group in groups:
            # Use 1-based indexing for consistency with formatters
            suggestion = {
                "group_id": group.group_id + 1,
                "suggested_filename": self._generate_filename_suggestion(graph, group),
                "functions": group.functions,
                "required_headers": self._identify_required_headers(graph, group.functions),
                "is_independent": group.is_independent,
                "has_cycles": group.has_cycles,
                "function_count": len(group.functions),
            }
            suggestions.append(suggestion)

        # Add warnings about imbalanced groups
        warnings = self._detect_imbalanced_groups(groups)
        if warnings:
            # Could add warnings to a separate field or log them
            pass

        return suggestions

    def _generate_filename_suggestion(
        self, graph: CallGraph, group: FunctionGroup
    ) -> str:
        """
        Generate a suggested filename based on the functions in the group.

        Args:
            graph: Call graph
            group: Function group

        Returns:
            Suggested filename (without extension)
        """
        if len(group.functions) == 0:
            return "unnamed_group"

        # Use the first function name as base
        first_func = group.functions[0]

        # Remove namespace/class qualifiers
        base_name = first_func.split("::")[-1]

        # If only one function, use its name
        if len(group.functions) == 1:
            return f"{base_name}"

        # For multiple functions, try to find common theme
        # Simple heuristic: use first function + "utils" or "group"
        if len(group.functions) <= 3:
            return f"{base_name}_utils"
        else:
            return f"{base_name}_group"

    def _identify_required_headers(
        self, graph: CallGraph, function_names: list[str]
    ) -> list[str]:
        """
        Identify required headers for a group of functions.

        Args:
            graph: Call graph
            function_names: List of function names in the group

        Returns:
            List of required header files
        """
        headers = set()

        for func_name in function_names:
            func = graph.functions.get(func_name)
            if not func:
                continue

            # Analyze signature for standard library types
            signature = func.signature.lower()

            # Common standard library includes
            if "std::string" in signature or "string" in signature:
                headers.add("<string>")
            if "std::vector" in signature or "vector" in signature:
                headers.add("<vector>")
            if "std::map" in signature or "map" in signature:
                headers.add("<map>")
            if "std::set" in signature or "set" in signature:
                headers.add("<set>")
            if "std::unique_ptr" in signature or "unique_ptr" in signature:
                headers.add("<memory>")
            if "std::shared_ptr" in signature or "shared_ptr" in signature:
                headers.add("<memory>")
            if "std::optional" in signature or "optional" in signature:
                headers.add("<optional>")
            if "std::iostream" in signature or "cout" in signature or "cin" in signature:
                headers.add("<iostream>")

        return sorted(headers)

    def _detect_imbalanced_groups(self, groups: list[FunctionGroup]) -> list[str]:
        """
        Detect imbalanced groups (e.g., one group much larger than others).

        Args:
            groups: List of function groups

        Returns:
            List of warning messages
        """
        if not groups:
            return []

        warnings = []
        function_counts = [len(g.functions) for g in groups]
        avg_size = sum(function_counts) / len(function_counts)
        max_size = max(function_counts)

        # Warn if largest group is more than 1.5x the average and has >10 functions
        if max_size > avg_size * 1.5 and max_size > 10:
            large_group = next(g for g in groups if len(g.functions) == max_size)
            warnings.append(
                f"Group {large_group.group_id} is significantly larger "
                f"({max_size} functions) than average ({avg_size:.1f}). "
                f"Consider further splitting this group."
            )

        return warnings
