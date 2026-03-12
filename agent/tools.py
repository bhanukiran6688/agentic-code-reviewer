"""
Tool implementations for the Code Review Agent.
"""

import ast
from pathlib import Path
from typing import Dict, Any

from observability.logger import logger


PROJECT_ROOT = Path.cwd()


class ToolExecutionError(Exception):
    """Raised when a tool fails."""


def _validate_path(path: str) -> Path:
    """
    Ensure path is within project root.
    """
    file_path = Path(path).resolve()

    if not str(file_path).startswith(str(PROJECT_ROOT)):
        raise ToolExecutionError("Access outside project directory denied.")

    if not file_path.exists():
        raise ToolExecutionError("File does not exist.")

    return file_path


def read_file(path: str) -> Dict[str, Any]:
    """
    Read file content safely.
    """
    file_path = _validate_path(path)

    try:
        content = file_path.read_text(encoding="utf-8")
        logger.info("Tool executed: read_file | %s", path)
        return {"status": "success", "content": content}
    except Exception as exc:
        raise ToolExecutionError(str(exc)) from exc


def count_lines(path: str) -> Dict[str, Any]:
    """
    Count total lines in file.
    """
    file_path = _validate_path(path)

    try:
        lines = file_path.read_text(encoding="utf-8").splitlines()
        logger.info("Tool executed: count_lines | %s", path)
        return {"status": "success", "line_count": len(lines)}
    except Exception as exc:
        raise ToolExecutionError(str(exc)) from exc


def analyze_complexity(path: str) -> Dict[str, Any]:
    """
    Analyze basic complexity using AST.
    Counts functions and classes.
    """
    file_path = _validate_path(path)

    try:
        source = file_path.read_text(encoding="utf-8")
        tree = ast.parse(source)

        functions = 0
        classes = 0

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions += 1
            elif isinstance(node, ast.ClassDef):
                classes += 1

        logger.info("Tool executed: analyze_complexity | %s", path)

        return {
            "status": "success",
            "functions": functions,
            "classes": classes,
        }

    except Exception as exc:
        raise ToolExecutionError(str(exc)) from exc


def simple_lint(path: str) -> Dict[str, Any]:
    """
    Basic linting checks:
    - Trailing whitespace
    - Long lines (> 120 chars)
    """
    file_path = _validate_path(path)

    try:
        issues = []
        lines = file_path.read_text(encoding="utf-8").splitlines()

        for idx, line in enumerate(lines, start=1):
            if line.rstrip() != line:
                issues.append(f"Line {idx}: Trailing whitespace")

            if len(line) > 120:
                issues.append(f"Line {idx}: Line exceeds 120 characters")

        logger.info("Tool executed: simple_lint | %s", path)

        return {
            "status": "success",
            "issues": issues,
            "issue_count": len(issues),
        }

    except Exception as exc:
        raise ToolExecutionError(str(exc)) from exc
