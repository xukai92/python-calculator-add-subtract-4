"""Tests for the calculator CLI."""

import subprocess
import sys

import pytest

from calculator.cli import main


class TestCLIParsing:
    def test_add(self, capsys: pytest.CaptureFixture[str]) -> None:
        main(["add", "2", "3"])
        assert capsys.readouterr().out.strip() == "2 + 3 = 5"

    def test_subtract(self, capsys: pytest.CaptureFixture[str]) -> None:
        main(["subtract", "10", "4"])
        assert capsys.readouterr().out.strip() == "10 - 4 = 6"

    def test_multiply(self, capsys: pytest.CaptureFixture[str]) -> None:
        main(["multiply", "3", "7"])
        assert capsys.readouterr().out.strip() == "3 * 7 = 21"

    def test_divide(self, capsys: pytest.CaptureFixture[str]) -> None:
        main(["divide", "20", "4"])
        assert capsys.readouterr().out.strip() == "20 / 4 = 5"

    def test_float_output(self, capsys: pytest.CaptureFixture[str]) -> None:
        main(["divide", "7", "2"])
        assert capsys.readouterr().out.strip() == "7 / 2 = 3.5"

    def test_divide_by_zero_exits(self) -> None:
        with pytest.raises(SystemExit, match="1"):
            main(["divide", "10", "0"])

    def test_invalid_operation(self) -> None:
        with pytest.raises(SystemExit):
            main(["modulo", "10", "3"])

    def test_missing_operand(self) -> None:
        with pytest.raises(SystemExit):
            main(["add", "10"])

    def test_non_numeric_operand(self) -> None:
        with pytest.raises(SystemExit):
            main(["add", "hello", "3"])


class TestCLIIntegration:
    def test_module_invocation(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "calculator", "add", "2", "3"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 0
        assert result.stdout.strip() == "2 + 3 = 5"

    def test_module_divide_by_zero(self) -> None:
        result = subprocess.run(
            [sys.executable, "-m", "calculator", "divide", "10", "0"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        assert result.returncode == 1
        assert "Cannot divide by zero" in result.stderr
