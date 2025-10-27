"""Data models for call graphs and metadata."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

import networkx as nx

from function_grouper.models.function import Function, SourceLocation


@dataclass
class CallEdge:
    """Represents a single directed edge in the call graph (caller → callee)."""

    caller: str
    callee: str
    call_count: int = 1
    call_locations: List[SourceLocation] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate call edge attributes."""
        if not self.caller:
            raise ValueError("caller must be non-empty")
        if not self.callee:
            raise ValueError("callee must be non-empty")
        if self.call_count < 1:
            raise ValueError(f"call_count must be >= 1, got {self.call_count}")


@dataclass
class GraphMetadata:
    """Contains summary information about the parsed file and resulting call graph."""

    source_file: str
    parse_timestamp: datetime
    total_functions: int
    successfully_parsed: int
    failed_to_parse: int
    total_call_edges: int
    total_groups: int
    independent_groups: int
    largest_group_size: int
    analysis_duration_seconds: float
    memory_used_mb: float

    def __post_init__(self) -> None:
        """Validate metadata attributes."""
        if self.total_functions < 0:
            raise ValueError(f"total_functions must be >= 0, got {self.total_functions}")
        if self.successfully_parsed < 0:
            raise ValueError(f"successfully_parsed must be >= 0, got {self.successfully_parsed}")
        if self.failed_to_parse < 0:
            raise ValueError(f"failed_to_parse must be >= 0, got {self.failed_to_parse}")
        if self.successfully_parsed + self.failed_to_parse != self.total_functions:
            raise ValueError(
                f"successfully_parsed ({self.successfully_parsed}) + "
                f"failed_to_parse ({self.failed_to_parse}) must equal "
                f"total_functions ({self.total_functions})"
            )


class CallGraph:
    """Represents the complete directed graph of function call relationships within a file."""

    def __init__(self) -> None:
        """Initialize an empty call graph."""
        self.functions: Dict[str, Function] = {}
        self.edges: List[CallEdge] = []
        self._graph: nx.DiGraph = nx.DiGraph()
        self.metadata: Optional[GraphMetadata] = None

    def add_function(self, func: Function) -> None:
        """Add a function node to the graph."""
        if func.qualified_name in self.functions:
            raise ValueError(f"Function {func.qualified_name} already exists in graph")
        self.functions[func.qualified_name] = func
        self._graph.add_node(func.qualified_name)

    def add_call(self, caller: str, callee: str, location: Optional[SourceLocation] = None) -> None:
        """Add a directed edge from caller to callee."""
        if caller not in self.functions:
            raise ValueError(f"Caller function {caller} not found in graph")
        if callee not in self.functions:
            # Only add edges for functions within the same file
            return

        # Check if edge already exists
        existing_edge = next((e for e in self.edges if e.caller == caller and e.callee == callee), None)

        if existing_edge:
            existing_edge.call_count += 1
            if location:
                existing_edge.call_locations.append(location)
        else:
            locations = [location] if location else []
            edge = CallEdge(caller=caller, callee=callee, call_locations=locations)
            self.edges.append(edge)
            self._graph.add_edge(caller, callee)

    def get_callers(self, func_name: str) -> List[str]:
        """Get all functions that call the specified function."""
        if func_name not in self.functions:
            raise ValueError(f"Function {func_name} not found in graph")
        return list(self._graph.predecessors(func_name))

    def get_callees(self, func_name: str) -> List[str]:
        """Get all functions called by the specified function."""
        if func_name not in self.functions:
            raise ValueError(f"Function {func_name} not found in graph")
        return list(self._graph.successors(func_name))

    def has_cycle(self) -> bool:
        """Check if the call graph contains cycles."""
        try:
            nx.find_cycle(self._graph)
            return True
        except nx.NetworkXNoCycle:
            return False

    def find_cycles(self) -> List[List[str]]:
        """Return all cycles in the graph."""
        try:
            cycles = list(nx.simple_cycles(self._graph))
            return cycles
        except Exception:
            return []

    def get_networkx_graph(self) -> nx.DiGraph:
        """Return the underlying NetworkX graph for advanced algorithms."""
        return self._graph

    def __len__(self) -> int:
        """Return the number of functions in the graph."""
        return len(self.functions)

    def __contains__(self, func_name: str) -> bool:
        """Check if a function exists in the graph."""
        return func_name in self.functions
