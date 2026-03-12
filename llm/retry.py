"""
Retry utilities with exponential backoff.
"""

import time
from typing import Callable, Any, Type

from observability.logger import logger
import config


class RetryException(Exception):
    """Raised when maximum retry attempts are exhausted."""


def retry(
    func: Callable[..., Any],
    exceptions: Type[Exception] | tuple[Type[Exception], ...],
    *args,
    **kwargs,
) -> Any:
    """
    Execute a function with exponential backoff retry logic.

    :param func: Function to execute
    :param exceptions: Exception(s) to retry on
    :param args: Positional args for function
    :param kwargs: Keyword args for function
    :return: Function result
    """
    attempt = 0
    delay = config.RETRY_BACKOFF_SECONDS

    while attempt < config.MAX_RETRIES:
        try:
            return func(*args, **kwargs)
        except exceptions as exc:
            attempt += 1
            logger.warning(
                "Retry attempt %s/%s failed: %s",
                attempt,
                config.MAX_RETRIES,
                str(exc),
            )

            if attempt >= config.MAX_RETRIES:
                logger.error("Max retries exhausted.")
                raise RetryException(str(exc)) from exc

            time.sleep(delay)
            delay *= 2  # Exponential backoff
    return None
