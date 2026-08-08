# Calculator

A production-quality Python calculator with add, subtract, multiply, and divide operations. Demonstrates modern Python best practices: src-layout packaging, type safety with mypy strict mode, comprehensive testing, and dual API/CLI interface.

## Installation

Requires Python 3.13+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Usage

### Python API

```python
from calculator import Calculator

calc = Calculator()

calc.add(2, 3)  # 5.0
calc.subtract(10, 4)  # 6.0
calc.multiply(3, 7)  # 21.0
calc.divide(20, 4)  # 5.0
```

Division by zero raises `ValueError`:

```python
calc.divide(1, 0)  # ValueError: Cannot divide by zero
```

Non-numeric inputs raise `TypeError`:

```python
calc.add("a", 1)  # TypeError: Expected numeric type, got str
```

### Command-Line Interface

```bash
uv run calculator add 2 3
# 2 + 3 = 5

uv run calculator subtract 10 4
# 10 - 4 = 6

uv run calculator multiply 3 7
# 3 * 7 = 21

uv run calculator divide 20 4
# 20 / 4 = 5
```

Or via `python -m`:

```bash
uv run python -m calculator add 2 3
```

## Testing

```bash
uv run pytest
```

With coverage report:

```bash
uv run pytest --cov
```

## Code Quality

```bash
uv run ruff check .   # lint
uv run ruff format .  # format
uv run mypy src/      # type check
```

## License

MIT
