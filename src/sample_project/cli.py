"""CLI module for sample project."""

from __future__ import annotations

import click

from sample_project import __version__


@click.group()
@click.version_option(version=__version__, prog_name="sample-cli")
def cli() -> None:
    """Sample CLI tool with useful commands."""
    pass


@cli.command()
@click.argument("name", default="World")
@click.option("--upper", "-u", is_flag=True, help="Convert to uppercase")
def greet(name: str, upper: bool) -> None:
    """Greet someone by name.

    Args:
        name: The name to greet
        upper: Whether to convert the greeting to uppercase
    """
    message = f"Hello, {name}!"
    if upper:
        message = message.upper()
    click.echo(message)


@cli.command()
@click.argument("numbers", nargs=-1, type=float)
def sum_numbers(numbers: tuple[float, ...]) -> None:
    """Sum a list of numbers.

    Args:
        numbers: Numbers to sum
    """
    if not numbers:
        click.echo("No numbers provided!")
        return
    result = sum(numbers)
    click.echo(f"Sum: {result}")


def main() -> None:
    """Entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
