"""Core calculator module with basic arithmetic operations."""


class Calculator:
    """A calculator supporting basic arithmetic operations."""

    def add(self, a: float, b: float) -> float:
        """Return the sum of a and b."""
        self._validate_inputs(a, b)
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Return the difference of a and b."""
        self._validate_inputs(a, b)
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Return the product of a and b."""
        self._validate_inputs(a, b)
        return a * b

    def divide(self, a: float, b: float) -> float:
        """Return the quotient of a divided by b."""
        self._validate_inputs(a, b)
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    @staticmethod
    def _validate_inputs(a: object, b: object) -> None:
        if not isinstance(a, (int, float)) or isinstance(a, bool):
            raise TypeError(f"Expected numeric type, got {type(a).__name__}")
        if not isinstance(b, (int, float)) or isinstance(b, bool):
            raise TypeError(f"Expected numeric type, got {type(b).__name__}")
