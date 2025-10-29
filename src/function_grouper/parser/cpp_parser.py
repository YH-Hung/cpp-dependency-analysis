"""C++ parser using libclang."""

import os

from clang.cindex import Index, TranslationUnit

from function_grouper.models import Function
from function_grouper.parser.function_extractor import FunctionExtractor


class CppParser:
    """Parses C++ source files using libclang to extract function definitions and calls."""

    def __init__(self, std_version: str = "c++17") -> None:
        """Initialize the C++ parser.

        Args:
            std_version: C++ standard version (default: c++17)
        """
        self.index: Index = Index.create()
        self.std_version = std_version
        self.include_paths: list[str] = []

    def add_include_path(self, path: str) -> None:
        """Add an include path for parsing.

        Args:
            path: Directory path to add to include search path
        """
        if os.path.isdir(path):
            self.include_paths.append(path)

    def parse_file(
        self,
        file_path: str,
        std_version: str | None = None,
    ) -> list[Function]:
        """Parse a C++ file and extract all function definitions.

        Args:
            file_path: Path to the C++ file to parse
            std_version: C++ standard version (overrides instance default)

        Returns:
            List of Function objects found in the file

        Raises:
            FileNotFoundError: If the file does not exist
            RuntimeError: If parsing fails
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Build compilation arguments
        args = [f"-std={std_version or self.std_version}"]
        for include_path in self.include_paths:
            args.append(f"-I{include_path}")

        # Parse the translation unit
        try:
            tu: TranslationUnit = self.index.parse(
                file_path,
                args=args,
                options=TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to parse {file_path}: {e}") from e

        # Check for fatal errors
        if tu is None:
            raise RuntimeError(f"Failed to create translation unit for {file_path}")

        # Extract functions using FunctionExtractor
        extractor = FunctionExtractor(file_path)
        functions = extractor.extract_functions(tu.cursor)

        return functions
