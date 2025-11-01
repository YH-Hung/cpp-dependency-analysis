"""JSON formatter for machine-readable output."""

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import psutil
from jsonschema import ValidationError, validate

from function_grouper.models.call_graph import CallGraph
from function_grouper.models.group import FunctionGroup


class JSONFormatter:
    """Format function groups as JSON with schema validation."""

    def __init__(self) -> None:
        """Initialize the formatter and load schema."""
        self._schema = self._load_schema()
        self._start_time = time.time()
        self._process = psutil.Process()
        self._start_memory = self._process.memory_info().rss / (1024 * 1024)  # MB

    def _load_schema(self) -> dict[str, Any]:
        """Load the JSON schema for validation."""
        # Try to find schema in specs directory
        schema_path = Path(__file__).parent.parent.parent.parent / "specs" / "001-function-grouper" / "contracts" / "json-output-schema.json"

        if schema_path.exists():
            with open(schema_path) as f:
                return json.load(f)

        # If not found, return minimal schema to avoid errors
        return {
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "required": ["metadata", "functions", "groups"],
        }

    def format(
        self,
        groups: list[FunctionGroup],
        call_graph: CallGraph,
        source_file: str,
        export_suggestions: list[dict[str, Any]] | None = None,
    ) -> str:
        """
        Format function groups as JSON conforming to json-output-schema.json.

        Args:
            groups: List of function groups
            call_graph: The complete call graph with functions and metadata
            source_file: Path to the source file analyzed
            export_suggestions: Optional export suggestions from ExportSuggester

        Returns:
            JSON string validated against schema
        """
        # Calculate elapsed time and memory
        duration_seconds = time.time() - self._start_time
        current_memory = self._process.memory_info().rss / (1024 * 1024)  # MB
        memory_used_mb = max(current_memory - self._start_memory, 0)

        # Calculate metadata statistics
        total_functions = len(call_graph.functions)
        successfully_parsed = sum(
            1 for f in call_graph.functions.values() if f.parse_status.name == "SUCCESS"
        )
        failed_to_parse = total_functions - successfully_parsed
        total_call_edges = len(call_graph.edges)
        independent_groups = sum(1 for group in groups if group.is_independent)
        largest_group_size = max((len(group.functions) for group in groups), default=0)

        # Build metadata
        metadata = {
            "source_file": str(Path(source_file).absolute()),
            "parse_timestamp": datetime.now(timezone.utc).isoformat(),
            "total_functions": total_functions,
            "successfully_parsed": successfully_parsed,
            "failed_to_parse": failed_to_parse,
            "total_call_edges": total_call_edges,
            "total_groups": len(groups),
            "independent_groups": independent_groups,
            "largest_group_size": largest_group_size,
            "analysis_duration_seconds": round(duration_seconds, 3),
            "memory_used_mb": round(memory_used_mb, 2),
        }

        # Build functions array
        functions_data = []
        for func in call_graph.functions.values():
            func_data = {
                "name": func.name,
                "qualified_name": func.qualified_name,
                "signature": func.signature,
                "location": {
                    "file": func.location.file_path,
                    "line": func.location.line_number,
                    "column": func.location.column_number,
                    "end_line": func.location.end_line_number,
                },
                "kind": func.kind.name,
                "calls": func.calls,
                "parse_status": func.parse_status.name,
            }

            # Add error message if present
            if hasattr(func, 'error_message') and func.error_message:
                func_data["error_message"] = func.error_message
            else:
                func_data["error_message"] = None

            functions_data.append(func_data)

        # Build groups array
        groups_data = []
        for i, group in enumerate(groups):
            group_data = {
                "group_id": i,
                "functions": sorted(group.functions),
                "is_independent": group.is_independent,
                "internal_edges": group.internal_edges,
                "external_edges": group.external_edges,
                "has_cycles": group.has_cycles,
            }
            groups_data.append(group_data)

        # Build complete output
        output: dict[str, Any] = {
            "metadata": metadata,
            "functions": functions_data,
            "groups": groups_data,
        }

        # Add parse errors if any
        parse_errors = []
        for func in call_graph.functions.values():
            if func.parse_status.name in ["PARTIAL", "FAILED"]:
                error_data = {
                    "function_name": func.name,
                    "location": {
                        "file": func.location.file_path,
                        "line": func.location.line_number,
                        "column": func.location.column_number,
                    },
                    "error": getattr(func, 'error_message', 'Unknown parse error'),
                }
                parse_errors.append(error_data)

        if parse_errors:
            output["parse_errors"] = parse_errors

        # Add export suggestions if provided
        if export_suggestions:
            output["export_suggestions"] = export_suggestions

        # Validate against schema
        try:
            validate(instance=output, schema=self._schema)
        except ValidationError as e:
            # Log validation error but don't fail - schema might be missing in some setups
            import sys
            print(f"Warning: JSON output validation failed: {e.message}", file=sys.stderr)

        return json.dumps(output, indent=2)
