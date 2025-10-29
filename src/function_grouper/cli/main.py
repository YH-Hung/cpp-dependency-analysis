"""Main CLI entry point for function-grouper."""

import sys
from pathlib import Path

import click

from function_grouper.analyzer.call_analyzer import CallAnalyzer
from function_grouper.analyzer.grouper import Grouper
from function_grouper.formatter.dot_formatter import DOTFormatter
from function_grouper.formatter.json_formatter import JSONFormatter
from function_grouper.formatter.text_formatter import TextFormatter
from function_grouper.parser.cpp_parser import CppParser


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
    "-v",
    "--verbose",
    count=True,
    help="Increase verbosity (-v, -vv, -vvv)",
)
@click.option(
    "--version",
    is_flag=True,
    is_eager=True,
    expose_value=False,
    callback=lambda ctx, param, value: (
        click.echo("function-grouper version 1.0.0"),
        click.echo(f"Python version: {sys.version.split()[0]}"),
        ctx.exit()
    ) if value else None,
    help="Show version and exit",
)
def main(
    input_file: str,
    format: str,
    output: str | None,
    std: str,
    include_paths: tuple,
    verbose: int,
) -> None:
    """
    Analyze C++ function dependencies and identify independent groups.

    INPUT_FILE: C++ implementation file (.cpp) to analyze
    """
    try:
        # Verbose output
        if verbose > 0:
            click.echo(f"Analyzing: {input_file}", err=True)
            click.echo(f"C++ Standard: {std}", err=True)
            if include_paths:
                click.echo(f"Include paths: {', '.join(include_paths)}", err=True)

        # Step 1: Parse the C++ file
        if verbose > 1:
            click.echo("Parsing C++ file...", err=True)

        parser = CppParser()
        functions = parser.parse_file(input_file, std_version=std)

        if verbose > 1:
            click.echo(f"Found {len(functions)} functions", err=True)

        # Step 2: Build call graph
        if verbose > 1:
            click.echo("Building call graph...", err=True)

        analyzer = CallAnalyzer()
        call_graph = analyzer.build_call_graph(functions)

        # Step 3: Find independent groups
        if verbose > 1:
            click.echo("Finding independent groups...", err=True)

        grouper = Grouper()
        groups = grouper.find_independent_groups(call_graph)

        if verbose > 0:
            click.echo(f"Found {len(groups)} groups", err=True)

        # Step 4: Format output
        if verbose > 1:
            click.echo(f"Formatting output as {format}...", err=True)

        if format == "text":
            formatter = TextFormatter()
            result = formatter.format(groups, input_file)
        elif format == "json":
            formatter = JSONFormatter()
            result = formatter.format(groups, input_file)
        elif format == "dot":
            formatter = DOTFormatter()
            result = formatter.format(groups, call_graph, input_file)
        else:
            click.echo(f"Error: Unknown format '{format}'", err=True)
            sys.exit(1)

        # Step 5: Output
        if output:
            output_path = Path(output)
            output_path.write_text(result)
            if verbose > 0:
                click.echo(f"Output written to: {output}", err=True)
        else:
            click.echo(result)

    except FileNotFoundError as e:
        click.echo(f"Error: File not found: {e}", err=True)
        sys.exit(2)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        if verbose > 2:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
