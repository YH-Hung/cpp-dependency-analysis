"""JSON formatter for machine-readable output."""

import json
from typing import List, Dict, Any
from function_grouper.models.group import FunctionGroup


class JSONFormatter:
    """Format function groups as JSON."""

    def format(self, groups: List[FunctionGroup], source_file: str) -> str:
        """
        Format function groups as JSON.

        Args:
            groups: List of function groups
            source_file: Path to the source file analyzed

        Returns:
            JSON string
        """
        # Calculate metadata
        total_functions = sum(len(group.functions) for group in groups)
        total_edges = sum(group.internal_edges for group in groups)

        output: Dict[str, Any] = {
            "metadata": {
                "source_file": source_file,
                "total_functions": total_functions,
                "total_groups": len(groups),
                "total_call_edges": total_edges,
            },
            "groups": []
        }

        # Add groups
        for i, group in enumerate(groups, 1):
            group_data = {
                "group_id": i,
                "functions": sorted(list(group.functions)),
                "is_independent": group.is_independent,
                "internal_edges": group.internal_edges,
                "external_edges": group.external_edges,
                "has_cycles": group.has_cycles,
            }
            output["groups"].append(group_data)

        return json.dumps(output, indent=2)
