"""Eval harness for the calculator project."""

import contextlib
import json
import subprocess
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(  # noqa: S603
        cmd, cwd=cwd, capture_output=True, text=True, timeout=120
    )


def score_tests(project: Path) -> tuple[float, dict[str, str]]:
    result = run(["uv", "run", "pytest", "--tb=short", "-q"], project)
    output = result.stdout + result.stderr
    if result.returncode == 5:
        return 0.3, {"status": "no tests collected", "detail": output.strip()[-500:]}
    if result.returncode == 0:
        return 1.0, {"status": "all passed", "detail": output.strip()[-500:]}
    for line in output.splitlines():
        if "passed" in line or "failed" in line:
            parts = line.split()
            passed = failed = 0
            for i, part in enumerate(parts):
                if part == "passed" and i > 0:
                    with contextlib.suppress(ValueError):
                        passed = int(parts[i - 1])
                if part == "failed" and i > 0:
                    with contextlib.suppress(ValueError):
                        failed = int(parts[i - 1])
            total = passed + failed
            if total > 0:
                return round(passed / total, 4), {
                    "status": f"{passed}/{total} passed",
                    "detail": output.strip()[-500:],
                }
    return 0.0, {"status": "error", "detail": output.strip()[-500:]}


def score_lint(project: Path) -> tuple[float, dict[str, str]]:
    result = run(["uv", "run", "ruff", "check", "."], project)
    output = result.stdout + result.stderr
    if result.returncode == 0:
        return 1.0, {"status": "clean", "detail": output.strip()[-500:]}
    lines = [
        line for line in output.splitlines()
        if line.strip() and not line.startswith("---")
    ]
    error_count = len([
        line for line in lines
        if ": " in line and not line.startswith("Found")
    ])
    return max(0.0, round(1.0 - error_count * 0.1, 4)), {
        "status": f"{error_count} issues",
        "detail": output.strip()[-500:],
    }


def score_type_check(project: Path) -> tuple[float, dict[str, str]]:
    result = run(["uv", "run", "mypy", "src/"], project)
    output = result.stdout + result.stderr
    if result.returncode == 0:
        return 1.0, {"status": "clean", "detail": output.strip()[-500:]}
    error_lines = [
        line for line in output.splitlines() if ": error:" in line
    ]
    error_count = len(error_lines)
    if error_count == 0:
        return 0.5, {"status": "warnings only", "detail": output.strip()[-500:]}
    return max(0.0, round(1.0 - error_count * 0.1, 4)), {
        "status": f"{error_count} errors",
        "detail": output.strip()[-500:],
    }


def score_coverage(project: Path) -> tuple[float, dict[str, str]]:
    result = run(
        [
            "uv", "run", "pytest",
            "--cov=calculator", "--cov-report=term-missing", "-q",
        ],
        project,
    )
    output = result.stdout + result.stderr
    if result.returncode == 5:
        return 0.0, {
            "status": "no tests",
            "detail": "no tests to measure coverage",
        }
    for line in output.splitlines():
        if "TOTAL" in line:
            parts = line.split()
            for part in parts:
                if part.endswith("%"):
                    with contextlib.suppress(ValueError):
                        pct = int(part.rstrip("%"))
                        return round(pct / 100.0, 4), {
                            "status": f"{pct}% coverage",
                            "detail": output.strip()[-500:],
                        }
    return 0.0, {"status": "unknown", "detail": output.strip()[-500:]}


def main() -> None:
    project = Path(__file__).resolve().parent.parent

    tests_score, tests_detail = score_tests(project)
    lint_score, lint_detail = score_lint(project)
    type_score, type_detail = score_type_check(project)
    cov_score, cov_detail = score_coverage(project)

    dimensions = {
        "tests": {"score": tests_score, **tests_detail},
        "lint": {"score": lint_score, **lint_detail},
        "type_check": {"score": type_score, **type_detail},
        "coverage": {"score": cov_score, **cov_detail},
    }

    weights = {"tests": 0.3, "lint": 0.2, "type_check": 0.2, "coverage": 0.3}
    composite = round(
        sum(dimensions[d]["score"] * weights[d] for d in weights), 4
    )

    result = {"composite": composite, "dimensions": dimensions}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
