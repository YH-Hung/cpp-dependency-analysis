"""Data models for C++ functions."""

from dataclasses import dataclass, field
from enum import Enum


class FunctionKind(Enum):
    """Categorizes the type of function definition."""

    FREE_FUNCTION = "FREE_FUNCTION"
    MEMBER_FUNCTION = "MEMBER_FUNCTION"
    STATIC_MEMBER_FUNCTION = "STATIC_MEMBER_FUNCTION"
    CONSTRUCTOR = "CONSTRUCTOR"
    DESTRUCTOR = "DESTRUCTOR"
    OPERATOR = "OPERATOR"
    LAMBDA = "LAMBDA"
    TEMPLATE_FUNCTION = "TEMPLATE_FUNCTION"
    TEMPLATE_SPECIALIZATION = "TEMPLATE_SPECIALIZATION"


class ParseStatus(Enum):
    """Indicates the parsing result for a function."""

    SUCCESS = "SUCCESS"
    PARTIAL = "PARTIAL"
    FAILED = "FAILED"


@dataclass(frozen=True)
class SourceLocation:
    """Represents the position of a function in the source code."""

    file_path: str
    line_number: int
    column_number: int
    end_line_number: int | None = None

    def __post_init__(self) -> None:
        """Validate source location attributes."""
        if self.line_number < 1:
            raise ValueError(f"line_number must be >= 1, got {self.line_number}")
        if self.column_number < 1:
            raise ValueError(f"column_number must be >= 1, got {self.column_number}")
        if self.end_line_number is not None and self.end_line_number < self.line_number:
            raise ValueError(
                f"end_line_number ({self.end_line_number}) must be >= "
                f"line_number ({self.line_number})"
            )


@dataclass
class Function:
    """Represents a single function definition found in the C++ source file."""

    name: str
    qualified_name: str
    signature: str
    location: SourceLocation
    kind: FunctionKind
    calls: list[str] = field(default_factory=list)
    parse_status: ParseStatus = ParseStatus.SUCCESS
    error_message: str | None = None

    def __post_init__(self) -> None:
        """Validate function attributes."""
        if not self.name:
            raise ValueError("name must be non-empty")
        if not self.qualified_name:
            raise ValueError("qualified_name must be non-empty")
        if (
            self.parse_status in (ParseStatus.FAILED, ParseStatus.PARTIAL)
            and self.error_message is None
        ):
            raise ValueError(
                f"error_message is required when parse_status is {self.parse_status.value}"
            )

    def add_call(self, callee_qualified_name: str) -> None:
        """Add a function call to the calls list."""
        if callee_qualified_name not in self.calls:
            self.calls.append(callee_qualified_name)

    def is_successfully_parsed(self) -> bool:
        """Return True if the function was successfully parsed."""
        return self.parse_status == ParseStatus.SUCCESS
