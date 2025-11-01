"""Text formatter for human-readable output."""

from typing import Any

from function_grouper.models.group import FunctionGroup


class TextFormatter:
    """Format function groups as human-readable text."""

    def format(
        self,
        groups: list[FunctionGroup],
        source_file: str,
        export_suggestions: list[dict[str, Any]] | None = None,
    ) -> str:
        """
        Format function groups as text.

        Args:
            groups: List of function groups
            source_file: Path to the source file analyzed
            export_suggestions: Optional export suggestions from ExportSuggester

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

        # Add export suggestions if provided
        if export_suggestions:
            lines.append("--- Export Suggestions ---")
            lines.append("")

            for suggestion in export_suggestions:
                group_id = suggestion["group_id"]
                filename = suggestion["suggested_filename"]
                func_count = suggestion["function_count"]
                headers = suggestion["required_headers"]
                is_independent = suggestion["is_independent"]

                lines.append(f"Group {group_id}: {filename}.cpp")
                lines.append(f"  Functions: {func_count}")
                lines.append(f"  Independent: {'Yes' if is_independent else 'No'}")

                if headers:
                    lines.append(f"  Required headers: {', '.join(headers)}")
                else:
                    lines.append("  Required headers: None detected")

                lines.append("")

        return "\n".join(lines)
