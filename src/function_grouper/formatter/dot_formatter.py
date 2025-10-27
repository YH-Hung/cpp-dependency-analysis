"""DOT formatter for Graphviz visualization."""

from typing import List, Set
from function_grouper.models.group import FunctionGroup
from function_grouper.models.call_graph import CallGraph


class DOTFormatter:
    """Format function groups as Graphviz DOT."""

    def format(
        self,
        groups: List[FunctionGroup],
        call_graph: CallGraph,
        source_file: str
    ) -> str:
        """
        Format function groups as DOT.

        Args:
            groups: List of function groups
            call_graph: The call graph with edges
            source_file: Path to the source file analyzed

        Returns:
            DOT format string
        """
        lines = []
        lines.append("digraph function_dependencies {")
        lines.append("  rankdir=LR;")
        lines.append("  node [shape=box];")
        lines.append("")

        # Create nodes for all functions
        all_functions: Set[str] = set()
        for group in groups:
            all_functions.update(group.functions)

        lines.append("  // Functions")
        for func in sorted(all_functions):
            # Escape quotes in function names
            escaped_name = func.replace('"', '\\"')
            label = func.split("::")[-1]  # Use short name for label
            lines.append(f'  "{escaped_name}" [label="{label}"];')

        lines.append("")

        # Create edges from call graph
        lines.append("  // Function calls")
        for edge in call_graph.edges:
            caller_escaped = edge.caller.replace('"', '\\"')
            callee_escaped = edge.callee.replace('"', '\\"')
            lines.append(f'  "{caller_escaped}" -> "{callee_escaped}";')

        lines.append("")

        # Create subgraphs for groups
        for i, group in enumerate(groups, 1):
            lines.append(f"  // Group {i}")
            lines.append(f"  subgraph cluster_{i} {{")
            lines.append(f'    label="Group {i}";')
            lines.append("    style=filled;")

            # Use different colors for groups with cycles
            if group.has_cycles:
                lines.append("    color=lightcoral;")
            else:
                lines.append("    color=lightgrey;")

            # Add functions to subgraph
            for func in sorted(group.functions):
                escaped_name = func.replace('"', '\\"')
                lines.append(f'    "{escaped_name}";')

            lines.append("  }")
            lines.append("")

        lines.append("}")
        return "\n".join(lines)
