"""
Structured logging configuration.
"""

import logging
import sys


def setup_logger() -> logging.Logger:
    """
    Configure and return a structured logger.
    """
    logger = logging.getLogger("agentic_code_reviewer")
    logger.setLevel(logging.INFO)

    if logger.handlers:
        return logger

    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.propagate = False

    return logger


logger = setup_logger()
