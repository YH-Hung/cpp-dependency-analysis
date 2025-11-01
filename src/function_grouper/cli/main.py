"""Main CLI entry point for function-grouper."""

import sys
from pathlib import Path

import click

from function_grouper.analyzer.call_analyzer import CallAnalyzer
from function_grouper.analyzer.export_suggester import ExportSuggester
from function_grouper.analyzer.grouper import Grouper
from function_grouper.formatter.dot_formatter import DOTFormatter
from function_grouper.formatter.json_formatter import JSONFormatter
from function_grouper.formatter.text_formatter import TextFormatter
from function_grouper.parser.cpp_parser import CppParser


def version_callback(ctx: click.Context, param: click.Parameter, value: bool) -> None:
    """Version callback for --version flag."""
    if value:
        click.echo("function-grouper version 1.0.0")
        click.echo(f"Python version: {sys.version.split()[0]}")
        ctx.exit()


@click.command()
@click.argument(
    "input_file",
    type=click.Path(exists=True, dir_okay=False, readable=True),
)
@click.option(
    "-f",
    "--format",
    type=click.Choice(["text", "json", "dot"], case_sensitive=False),
    default="text",
    help="Output format (default: text)",
)
@click.option(
    "-o",
    "--output",
    type=click.Path(dir_okay=False, writable=True),
    default=None,
    help="Output file (default: stdout)",
)
@click.option(
    "--std",
    type=click.Choice(["c++11", "c++14", "c++17", "c++20", "c++23"]),
    default="c++17",
    help="C++ standard version (default: c++17)",
)
@click.option(
    "-I",
    "--include",
    "include_paths",
    multiple=True,
    type=click.Path(exists=True, file_okay=False, dir_okay=True),
    help="Include directory (repeatable)",
)
@click.option(
    "--progress/--no-progress",
    default=True,
    help="Show/hide progress indication (default: enabled)",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Increase verbosity (-v, -vv, -vvv)",
)
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    default=False,
    help="Suppress all output except errors (mutually exclusive with --verbose)",
)
@click.option(
    "--strict/--no-strict",
    default=False,
    help="Fail if any function cannot be parsed (default: lenient)",
)
@click.option(
    "--force",
    is_flag=True,
    default=False,
    help="Overwrite output file without confirmation",
)
@click.option(
    "--export-suggestions",
    is_flag=True,
    default=False,
    help="Include file split suggestions based on independent groups",
)
@click.option(
    "--version",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=version_callback,
    help="Show version and exit",
)
def main(
    input_file: str,
    format: str,
    output: str | None,
    std: str,
    include_paths: tuple[str, ...],
    progress: bool,
    verbose: int,
    quiet: bool,
    strict: bool,
    force: bool,
    export_suggestions: bool,
) -> None:
    """
    Analyze C++ function dependencies and identify independent groups.

    INPUT_FILE: C++ implementation file (.cpp) to analyze
    """
    try:
        # Validate mutual exclusivity of quiet and verbose
        if quiet and verbose > 0:
            click.echo("Error: --quiet and --verbose are mutually exclusive", err=True)
            sys.exit(5)  # INVALID_ARGUMENTS

        # Check if output file exists and prompt for confirmation unless --force
        if output and not force:
            output_path = Path(output)
            if output_path.exists():
                if not click.confirm(f"Output file {output} already exists. Overwrite?"):
                    click.echo("Aborted.", err=True)
                    sys.exit(0)

        # Verbose output
        if verbose > 0 and not quiet:
            click.echo(f"Analyzing: {input_file}", err=True)
            click.echo(f"C++ Standard: {std}", err=True)
            if include_paths:
                click.echo(f"Include paths: {', '.join(include_paths)}", err=True)

        # Step 1: Parse the C++ file
        if verbose > 1 and not quiet:
            click.echo("Parsing C++ file...", err=True)

        parser = CppParser()
        functions = parser.parse_file(input_file, std_version=std)

        if verbose > 1 and not quiet:
            click.echo(f"Found {len(functions)} functions", err=True)

        # Check for parse failures in strict mode
        failed_functions = [f for f in functions if f.parse_status.name != "SUCCESS"]
        if strict and failed_functions:
            click.echo(
                f"Error: Strict mode enabled. Failed to parse {len(failed_functions)} function(s)",
                err=True
            )
            for func in failed_functions:
                error_msg = getattr(func, 'error_message', 'Unknown error')
                click.echo(
                    f"  - {func.qualified_name} at line {func.location.line_number}: {error_msg}",
                    err=True
                )
            sys.exit(4)  # PARSE_ERROR

        # Step 2: Build call graph
        if verbose > 1 and not quiet:
            click.echo("Building call graph...", err=True)

        analyzer = CallAnalyzer()
        call_graph = analyzer.build_call_graph(functions)

        # Step 3: Find independent groups
        if verbose > 1 and not quiet:
            click.echo("Finding independent groups...", err=True)

        grouper = Grouper()
        groups = grouper.find_independent_groups(call_graph)

        if verbose > 0 and not quiet:
            click.echo(f"Found {len(groups)} groups", err=True)

        # Step 3.5: Generate export suggestions if requested
        suggestions = None
        if export_suggestions:
            if verbose > 1 and not quiet:
                click.echo("Generating export suggestions...", err=True)
            suggester = ExportSuggester()
            suggestions = suggester.suggest_file_splits(call_graph, groups)

        # Step 4: Format output
        if verbose > 1 and not quiet:
            click.echo(f"Formatting output as {format}...", err=True)

        result: str
        if format == "text":
            formatter = TextFormatter()
            result = formatter.format(groups, input_file, suggestions)
        elif format == "json":
            json_formatter = JSONFormatter()
            result = json_formatter.format(groups, call_graph, input_file, suggestions)
        elif format == "dot":
            dot_formatter = DOTFormatter()
            result = dot_formatter.format(groups, call_graph, input_file)
        else:
            click.echo(f"Error: Unknown format '{format}'", err=True)
            sys.exit(1)

        # Step 5: Output
        if output:
            output_path = Path(output)
            output_path.write_text(result)
            if verbose > 0 and not quiet:
                click.echo(f"Output written to: {output}", err=True)
        else:
            click.echo(result)

    except FileNotFoundError as e:
        click.echo(f"Error: File not found: {e}", err=True)
        sys.exit(2)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        # Show traceback if verbose, but respect the function signature
        # Note: verbose might not be defined if error occurs before argument parsing
        try:
            if verbose > 2 and not quiet:
                import traceback
                traceback.print_exc()
        except NameError:
            # verbose not defined yet, skip traceback
            pass
        sys.exit(1)


if __name__ == "__main__":
    main()
