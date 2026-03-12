"""
Security-focused safety validation for generated reviews.
"""

import re
from typing import Dict, Any


class SafetyViolation(Exception):
    """Raised when unsafe review content is detected."""


class SafetyChecker:
    """
    Performs post-generation security checks.
    """

    DANGEROUS_PATTERNS = [
        r"disable authentication",
        r"remove validation",
        r"turn off security",
        r"set debug\s*=\s*true",
        r"allow all origins",
        r"chmod\s+777",
    ]

    @classmethod
    def validate_review(cls, review_text: str) -> Dict[str, Any]:
        """
        Validate generated review for unsafe recommendations.
        """
        issues = []

        lower_text = review_text.lower()

        for pattern in cls.DANGEROUS_PATTERNS:
            if re.search(pattern, lower_text):
                issues.append(
                    f"Potential unsafe suggestion detected: {pattern}"
                )

        return {
            "safe": len(issues) == 0,
            "issues": issues,
        }
