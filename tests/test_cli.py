"""Tests for CLI module."""

import pytest
from click.testing import CliRunner

from sample_project.cli import cli


@pytest.fixture
def runner() -> CliRunner:
    """Create a CLI runner for testing."""
    return CliRunner()


class TestGreetCommand:
    """Tests for the greet command."""

    def test_greet_default(self, runner: CliRunner) -> None:
        """Test greet with default name."""
        result = runner.invoke(cli, ["greet"])
        assert result.exit_code == 0
        assert "Hello, World!" in result.output

    def test_greet_with_name(self, runner: CliRunner) -> None:
        """Test greet with custom name."""
        result = runner.invoke(cli, ["greet", "Alice"])
        assert result.exit_code == 0
        assert "Hello, Alice!" in result.output

    def test_greet_uppercase(self, runner: CliRunner) -> None:
        """Test greet with uppercase flag."""
        result = runner.invoke(cli, ["greet", "Bob", "--upper"])
        assert result.exit_code == 0
        assert "HELLO, BOB!" in result.output


class TestSumCommand:
    """Tests for the sum command."""

    def test_sum_numbers(self, runner: CliRunner) -> None:
        """Test sum with multiple numbers."""
        result = runner.invoke(cli, ["sum-numbers", "1", "2", "3"])
        assert result.exit_code == 0
        assert "Sum: 6.0" in result.output

    def test_sum_no_numbers(self, runner: CliRunner) -> None:
        """Test sum with no numbers."""
        result = runner.invoke(cli, ["sum-numbers"])
        assert result.exit_code == 0
        assert "No numbers provided!" in result.output


class TestVersion:
    """Tests for version flag."""

    def test_version(self, runner: CliRunner) -> None:
        """Test version output."""
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "sample-cli" in result.output
        assert "0.1.0" in result.output
