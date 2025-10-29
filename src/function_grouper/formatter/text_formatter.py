"""Text formatter for human-readable output."""


from function_grouper.models.group import FunctionGroup


class TextFormatter:
    """Format function groups as human-readable text."""

    def format(self, groups: list[FunctionGroup], source_file: str) -> str:
        """
        Format function groups as text.

        Args:
            groups: List of function groups
            source_file: Path to the source file analyzed

        Returns:
            Formatted text string
        """
        lines = []
        lines.append("=== C++ Function Grouper Analysis ===")
        lines.append("")
        lines.append(f"File: {source_file}")

        # Calculate totals
        total_functions = sum(len(group.functions) for group in groups)
        lines.append(f"Total Functions: {total_functions}")
        lines.append(f"Function Groups: {len(groups)}")
        lines.append("")

        # Display groups
        lines.append("--- Function Groups ---")
        lines.append("")

        for i, group in enumerate(groups, 1):
            func_count = len(group.functions)
            lines.append(f"Group {i} ({func_count} function{'s' if func_count != 1 else ''})")

            # List functions
            for func_name in sorted(group.functions):
                lines.append(f"  {func_name}")

            # Show group statistics
            lines.append(f"  Internal calls: {group.internal_edges}")

            if group.external_edges > 0:
                lines.append(f"  External calls: {group.external_edges}")

            if group.has_cycles:
                lines.append("  ⚠️  Contains circular dependencies")

            lines.append("")

        return "\n".join(lines)
