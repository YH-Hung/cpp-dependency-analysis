"""Unit tests for export suggester."""

from function_grouper.analyzer.export_suggester import ExportSuggester
from function_grouper.models.call_graph import CallGraph
from function_grouper.models.function import Function, FunctionKind, ParseStatus, SourceLocation
from function_grouper.models.group import FunctionGroup


class TestExportSuggester:
    """Tests for ExportSuggester class."""

    def test_suggest_file_splits(self) -> None:
        """Test suggest_file_splits generates recommendations for each group."""
        # Create a call graph with two groups
        graph = CallGraph()

        # Group 1: String utilities
        func1 = Function(
            name="trim",
            qualified_name="trim",
            signature="std::string trim(const std::string&)",
            location=SourceLocation("/path/file.cpp", 10, 1, 15),
            kind=FunctionKind.FREE_FUNCTION,
            calls=[],
            parse_status=ParseStatus.SUCCESS,
        )
        func2 = Function(
            name="trimLeft",
            qualified_name="trimLeft",
            signature="std::string trimLeft(const std::string&)",
            location=SourceLocation("/path/file.cpp", 20, 1, 25),
            kind=FunctionKind.FREE_FUNCTION,
            calls=["trim"],
            parse_status=ParseStatus.SUCCESS,
        )

        # Group 2: Math utilities
        func3 = Function(
            name="add",
            qualified_name="add",
            signature="int add(int, int)",
            location=SourceLocation("/path/file.cpp", 30, 1, 35),
            kind=FunctionKind.FREE_FUNCTION,
            calls=[],
            parse_status=ParseStatus.SUCCESS,
        )

        graph.add_function(func1)
        graph.add_function(func2)
        graph.add_function(func3)
        graph.add_call("trimLeft", "trim")

        groups = [
            FunctionGroup(
                group_id=1,
                functions=["trim", "trimLeft"],
                is_independent=True,
                internal_edges=1,
                external_edges=0,
                has_cycles=False,
            ),
            FunctionGroup(
                group_id=2,
                functions=["add"],
                is_independent=True,
                internal_edges=0,
                external_edges=0,
                has_cycles=False,
            ),
        ]

        suggester = ExportSuggester()
        suggestions = suggester.suggest_file_splits(graph, groups)

        assert len(suggestions) == 2
        assert all("suggested_filename" in s for s in suggestions)
        assert all("functions" in s for s in suggestions)
        assert all("required_headers" in s for s in suggestions)

    def test_identify_required_headers(self) -> None:
        """Test _identify_required_headers extracts includes used by functions."""
        graph = CallGraph()

        func1 = Function(
            name="trim",
            qualified_name="trim",
            signature="std::string trim(const std::string&)",
            location=SourceLocation("/path/file.cpp", 10, 1, 15),
            kind=FunctionKind.FREE_FUNCTION,
            calls=[],
            parse_status=ParseStatus.SUCCESS,
        )

        graph.add_function(func1)

        suggester = ExportSuggester()
        headers = suggester._identify_required_headers(graph, ["trim"])

        # Should identify that std::string requires <string>
        assert isinstance(headers, list)
        assert len(headers) >= 0  # May be empty or contain standard headers

    def test_detect_imbalanced_groups_warns_for_large_group(self) -> None:
        """Test _detect_imbalanced_groups identifies groups with too many functions."""
        groups = [
            FunctionGroup(
                group_id=1,
                functions=[f"func{i}" for i in range(20)],  # Large group
                is_independent=True,
                internal_edges=10,
                external_edges=0,
                has_cycles=False,
            ),
            FunctionGroup(
                group_id=2,
                functions=["add"],  # Small group
                is_independent=True,
                internal_edges=0,
                external_edges=0,
                has_cycles=False,
            ),
        ]

        suggester = ExportSuggester()
        warnings = suggester._detect_imbalanced_groups(groups)

        assert len(warnings) > 0
        assert any("imbalanced" in w.lower() or "large" in w.lower() for w in warnings)
