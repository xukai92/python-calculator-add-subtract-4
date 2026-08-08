"""Command-line interface for the calculator."""

import argparse
import sys

from calculator.calculator import Calculator


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="calculator",
        description="A simple calculator supporting basic arithmetic operations.",
    )
    parser.add_argument(
        "operation",
        choices=["add", "subtract", "multiply", "divide"],
        help="The arithmetic operation to perform",
    )
    parser.add_argument("operand1", type=float, help="First operand")
    parser.add_argument("operand2", type=float, help="Second operand")
    return parser


OP_SYMBOLS = {
    "add": "+",
    "subtract": "-",
    "multiply": "*",
    "divide": "/",
}


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    calc = Calculator()
    op_func = getattr(calc, args.operation)

    try:
        result = op_func(args.operand1, args.operand2)
    except (ValueError, TypeError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    symbol = OP_SYMBOLS[args.operation]
    a = int(args.operand1) if args.operand1 == int(args.operand1) else args.operand1
    b = int(args.operand2) if args.operand2 == int(args.operand2) else args.operand2
    r = int(result) if result == int(result) else result
    print(f"{a} {symbol} {b} = {r}")
