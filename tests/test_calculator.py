"""Tests for the Calculator class."""

import pytest

from calculator import Calculator


@pytest.fixture
def calc() -> Calculator:
    return Calculator()


class TestAdd:
    @pytest.mark.parametrize(
        ("a", "b", "expected"),
        [
            (2, 3, 5),
            (0, 0, 0),
            (-1, 1, 0),
            (-3, -7, -10),
            (0.1, 0.2, pytest.approx(0.3)),
            (1_000_000, 2_000_000, 3_000_000),
        ],
    )
    def test_add(self, calc: Calculator, a: float, b: float, expected: float) -> None:
        assert calc.add(a, b) == expected


class TestSubtract:
    @pytest.mark.parametrize(
        ("a", "b", "expected"),
        [
            (10, 4, 6),
            (0, 0, 0),
            (-1, -1, 0),
            (5, 8, -3),
            (0.3, 0.1, pytest.approx(0.2)),
            (1_000_000, 999_999, 1),
        ],
    )
    def test_subtract(
        self, calc: Calculator, a: float, b: float, expected: float
    ) -> None:
        assert calc.subtract(a, b) == expected


class TestMultiply:
    @pytest.mark.parametrize(
        ("a", "b", "expected"),
        [
            (3, 7, 21),
            (0, 100, 0),
            (-2, 3, -6),
            (-4, -5, 20),
            (0.5, 0.5, pytest.approx(0.25)),
            (100_000, 100_000, 10_000_000_000),
        ],
    )
    def test_multiply(
        self, calc: Calculator, a: float, b: float, expected: float
    ) -> None:
        assert calc.multiply(a, b) == expected


class TestDivide:
    @pytest.mark.parametrize(
        ("a", "b", "expected"),
        [
            (20, 4, 5.0),
            (1, 3, pytest.approx(0.333333, rel=1e-4)),
            (-10, 2, -5.0),
            (-6, -3, 2.0),
            (0, 5, 0.0),
            (7, 2, 3.5),
        ],
    )
    def test_divide(
        self, calc: Calculator, a: float, b: float, expected: float
    ) -> None:
        assert calc.divide(a, b) == expected

    def test_divide_by_zero(self, calc: Calculator) -> None:
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calc.divide(10, 0)


class TestInputValidation:
    @pytest.mark.parametrize("method", ["add", "subtract", "multiply", "divide"])
    def test_string_input_first_arg(self, calc: Calculator, method: str) -> None:
        with pytest.raises(TypeError, match="Expected numeric type"):
            getattr(calc, method)("hello", 1)

    @pytest.mark.parametrize("method", ["add", "subtract", "multiply", "divide"])
    def test_string_input_second_arg(self, calc: Calculator, method: str) -> None:
        with pytest.raises(TypeError, match="Expected numeric type"):
            getattr(calc, method)(1, "world")

    @pytest.mark.parametrize("method", ["add", "subtract", "multiply", "divide"])
    def test_none_input(self, calc: Calculator, method: str) -> None:
        with pytest.raises(TypeError, match="Expected numeric type"):
            getattr(calc, method)(None, 1)

    @pytest.mark.parametrize("method", ["add", "subtract", "multiply", "divide"])
    def test_bool_input(self, calc: Calculator, method: str) -> None:
        with pytest.raises(TypeError, match="Expected numeric type"):
            getattr(calc, method)(True, 1)


class TestInvariants:
    def test_add_commutative(self, calc: Calculator) -> None:
        assert calc.add(3, 7) == calc.add(7, 3)

    def test_multiply_commutative(self, calc: Calculator) -> None:
        assert calc.multiply(4, 5) == calc.multiply(5, 4)

    def test_add_subtract_inverse(self, calc: Calculator) -> None:
        a, b = 42, 17
        assert calc.subtract(calc.add(a, b), b) == a

    def test_multiply_divide_inverse(self, calc: Calculator) -> None:
        a, b = 42, 7
        assert calc.divide(calc.multiply(a, b), b) == pytest.approx(a)

    def test_add_identity(self, calc: Calculator) -> None:
        assert calc.add(5, 0) == 5

    def test_multiply_identity(self, calc: Calculator) -> None:
        assert calc.multiply(5, 1) == 5
