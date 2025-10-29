"""Data models for function groups."""

from dataclasses import dataclass, field


@dataclass
class FunctionGroup:
    """
    Represents a collection of functions connected through direct/indirect calls.
    """

    group_id: int
    functions: list[str] = field(default_factory=list)
    is_independent: bool = False
    internal_edges: int = 0
    external_edges: int = 0
    has_cycles: bool = False

    def __post_init__(self) -> None:
        """Validate function group attributes."""
        if self.group_id < 0:
            raise ValueError(f"group_id must be >= 0, got {self.group_id}")
        if not self.functions:
            raise ValueError("functions list must be non-empty")
        if self.internal_edges < 0:
            raise ValueError(f"internal_edges must be >= 0, got {self.internal_edges}")
        if self.external_edges < 0:
            raise ValueError(f"external_edges must be >= 0, got {self.external_edges}")
        if self.is_independent and self.external_edges > 0:
            raise ValueError("Independent groups cannot have external edges")

    def add_function(self, qualified_name: str) -> None:
        """Add a function to this group."""
        if qualified_name not in self.functions:
            self.functions.append(qualified_name)

    def size(self) -> int:
        """Return the number of functions in this group."""
        return len(self.functions)

    def __len__(self) -> int:
        """Return the number of functions in this group."""
        return len(self.functions)

    def __contains__(self, func_name: str) -> bool:
        """Check if a function is in this group."""
        return func_name in self.functions
