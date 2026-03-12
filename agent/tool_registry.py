"""
Tool registry and Gemini tool schema definitions.
"""

from typing import Callable, Dict, Any

from agent.tools import (
    read_file,
    count_lines,
    analyze_complexity,
    simple_lint,
)


# =========================
# Tool Execution Map
# =========================

TOOL_MAP: Dict[str, Callable[..., Dict[str, Any]]] = {
    "read_file": read_file,
    "count_lines": count_lines,
    "analyze_complexity": analyze_complexity,
    "simple_lint": simple_lint,
}


# =========================
# Gemini Tool Schemas
# =========================

TOOLS_SCHEMA = [
    {
        "name": "read_file",
        "description": "Read the contents of a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path to file",
                }
            },
            "required": ["path"],
        },
    },
    {
        "name": "count_lines",
        "description": "Count total lines in a file.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "analyze_complexity",
        "description": "Analyze number of functions and classes.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
            },
            "required": ["path"],
        },
    },
    {
        "name": "simple_lint",
        "description": "Perform simple lint checks.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
            },
            "required": ["path"],
        },
    },
]


def execute_tool(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a registered tool safely.
    """
    if name not in TOOL_MAP:
        raise ValueError(f"Unknown tool: {name}")

    return TOOL_MAP[name](**arguments)
