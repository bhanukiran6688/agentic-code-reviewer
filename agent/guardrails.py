"""
Centralized guardrails for agent safety.
"""

import re
from typing import Dict, Any

from observability.logger import logger


class GuardrailViolation(Exception):
    """Raised when a guardrail rule is violated."""


class Guardrails:
    """
    Safety enforcement layer for:
    - Tool execution
    - Prompt injection detection
    - Output validation
    """

    FORBIDDEN_PATTERNS = [
        r"rm\s+-rf",
        r"os\.system",
        r"subprocess",
        r"eval\(",
        r"exec\(",
        r"__import__",
    ]

    PROMPT_INJECTION_PATTERNS = [
        r"ignore previous instructions",
        r"disregard above rules",
        r"system prompt",
        r"override safety",
    ]

    @staticmethod
    def validate_tool_call(
        tool_name: str,
        arguments: Dict[str, Any],
    ) -> None:
        """
        Validate tool call before execution.
        """
        if not isinstance(arguments, dict):
            raise GuardrailViolation("Tool arguments must be a dictionary.")

        if tool_name not in {
            "read_file",
            "count_lines",
            "analyze_complexity",
            "simple_lint",
        }:
            raise GuardrailViolation(f"Unauthorized tool: {tool_name}")

        logger.info(
            "Guardrails: Tool call validated | %s",
            tool_name,
        )

    @classmethod
    def detect_prompt_injection(cls, text: str) -> None:
        """
        Detect common prompt injection attempts.
        """
        lower_text = text.lower()

        for pattern in cls.PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, lower_text):
                raise GuardrailViolation(
                    "Potential prompt injection detected."
                )

    @classmethod
    def validate_output(cls, text: str) -> None:
        """
        Validate final LLM output for unsafe suggestions.
        """
        for pattern in cls.FORBIDDEN_PATTERNS:
            if re.search(pattern, text):
                raise GuardrailViolation(
                    f"Unsafe pattern detected in output: {pattern}"
                )

        logger.info("Guardrails: Output validated.")
