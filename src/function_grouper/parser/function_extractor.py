"""Function extractor helper for parsing C++ AST."""


from clang.cindex import Cursor, CursorKind

from function_grouper.models import Function, FunctionKind, ParseStatus, SourceLocation


class FunctionExtractor:
    """Helper class to extract function definitions from C++ AST."""

    def __init__(self, source_file: str) -> None:
        """Initialize the function extractor.

        Args:
            source_file: Path to the source file being parsed
        """
        self.source_file = source_file
        self.functions: list[Function] = []
        self.function_names: set[str] = set()

    def extract_functions(self, cursor: Cursor) -> list[Function]:
        """Extract all function definitions from the AST.

        Args:
            cursor: Root cursor of the translation unit

        Returns:
            List of extracted Function objects
        """
        self.functions = []
        self.function_names = set()
        self._traverse(cursor)
        return self.functions

    def _traverse(self, cursor: Cursor) -> None:
        """Recursively traverse the AST to find function definitions.

        Args:
            cursor: Current cursor node
        """
        # Only process nodes from the main file (not includes)
        if cursor.location.file and cursor.location.file.name != self.source_file:
            return

        # Check if this is a function definition
        if self._is_function_definition(cursor):
            try:
                func = self._extract_function(cursor)
                self.functions.append(func)
                self.function_names.add(func.qualified_name)
            except Exception as e:
                # Create a partially parsed function on error
                try:
                    loc = SourceLocation(
                        file_path=self.source_file,
                        line_number=cursor.location.line,
                        column_number=cursor.location.column,
                    )
                    error_func = Function(
                        name=cursor.spelling or "unknown",
                        qualified_name=cursor.spelling or "unknown",
                        signature=cursor.displayname or "",
                        location=loc,
                        kind=FunctionKind.FREE_FUNCTION,
                        parse_status=ParseStatus.FAILED,
                        error_message=str(e),
                    )
                    self.functions.append(error_func)
                except Exception:
                    # If we can't even create an error function, skip it
                    pass

        # Recurse into children
        for child in cursor.get_children():
            self._traverse(child)

    def _is_function_definition(self, cursor: Cursor) -> bool:
        """Check if the cursor represents a function definition.

        Args:
            cursor: Cursor to check

        Returns:
            True if this is a function definition
        """
        return cursor.kind in (
            CursorKind.FUNCTION_DECL,
            CursorKind.CXX_METHOD,
            CursorKind.CONSTRUCTOR,
            CursorKind.DESTRUCTOR,
            CursorKind.FUNCTION_TEMPLATE,
        ) and cursor.is_definition()

    def _extract_function(self, cursor: Cursor) -> Function:
        """Extract a Function object from a cursor.

        Args:
            cursor: Cursor representing a function definition

        Returns:
            Function object

        Raises:
            Exception: If extraction fails
        """
        # Determine function kind
        kind = self._determine_function_kind(cursor)

        # Build qualified name
        qualified_name = self._build_qualified_name(cursor)

        # Get location
        location = SourceLocation(
            file_path=self.source_file,
            line_number=cursor.location.line,
            column_number=cursor.location.column,
            end_line_number=cursor.extent.end.line,
        )

        # Extract function calls
        calls = self._extract_calls(cursor)

        return Function(
            name=cursor.spelling,
            qualified_name=qualified_name,
            signature=cursor.displayname,
            location=location,
            kind=kind,
            calls=calls,
            parse_status=ParseStatus.SUCCESS,
        )

    def _determine_function_kind(self, cursor: Cursor) -> FunctionKind:
        """Determine the type of function.

        Args:
            cursor: Function cursor

        Returns:
            FunctionKind enum value
        """
        if cursor.kind == CursorKind.CONSTRUCTOR:
            return FunctionKind.CONSTRUCTOR
        elif cursor.kind == CursorKind.DESTRUCTOR:
            return FunctionKind.DESTRUCTOR
        elif cursor.kind == CursorKind.FUNCTION_TEMPLATE:
            return FunctionKind.TEMPLATE_FUNCTION
        elif cursor.kind == CursorKind.CXX_METHOD:
            # Check if static
            if cursor.is_static_method():
                return FunctionKind.STATIC_MEMBER_FUNCTION
            else:
                return FunctionKind.MEMBER_FUNCTION
        else:
            # Check if it's an operator overload
            if cursor.spelling.startswith("operator"):
                return FunctionKind.OPERATOR
            return FunctionKind.FREE_FUNCTION

    def _build_qualified_name(self, cursor: Cursor) -> str:
        """Build the fully qualified name of a function.

        Args:
            cursor: Function cursor

        Returns:
            Fully qualified name (e.g., "Namespace::Class::method")
        """
        parts: list[str] = []
        current = cursor

        # Walk up the semantic parent chain
        while current is not None:
            if current.kind in (
                CursorKind.NAMESPACE,
                CursorKind.CLASS_DECL,
                CursorKind.STRUCT_DECL,
                CursorKind.CLASS_TEMPLATE,
            ):
                if current.spelling:
                    parts.insert(0, current.spelling)
            elif current == cursor:
                # This is the function itself
                parts.append(cursor.spelling)

            current = current.semantic_parent

        if not parts:
            return str(cursor.spelling)

        return "::".join(parts)

    def _extract_calls(self, cursor: Cursor) -> list[str]:
        """Extract function calls from within a function body.

        Args:
            cursor: Function cursor

        Returns:
            List of qualified names of called functions
        """
        calls: list[str] = []
        self._find_calls_recursive(cursor, calls)
        return calls

    def _find_calls_recursive(self, cursor: Cursor, calls: list[str]) -> None:
        """Recursively find all CALL_EXPR nodes.

        Args:
            cursor: Current cursor
            calls: List to accumulate call names
        """
        if cursor.kind == CursorKind.CALL_EXPR:
            # Get the referenced function
            ref = cursor.referenced
            if ref and ref.kind in (
                CursorKind.FUNCTION_DECL,
                CursorKind.CXX_METHOD,
                CursorKind.CONSTRUCTOR,
                CursorKind.DESTRUCTOR,
            ):
                qualified_name = self._build_qualified_name(ref)
                if qualified_name and qualified_name not in calls:
                    calls.append(qualified_name)

        # Recurse into children
        for child in cursor.get_children():
            self._find_calls_recursive(child, calls)
