"""
Circuit breaker implementation for LLM failures.
"""

import time
from observability.logger import logger
import config


class CircuitBreakerOpen(Exception):
    """Raised when circuit breaker is open."""


class CircuitBreaker:
    """
    Basic circuit breaker pattern.
    """

    def __init__(self):
        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"

    def record_success(self) -> None:
        self.failure_count = 0
        self.state = "CLOSED"

    def record_failure(self) -> None:
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.failure_count >= config.CIRCUIT_BREAKER_FAILURE_THRESHOLD:
            self.state = "OPEN"
            logger.error("Circuit breaker opened.")

    def allow_request(self) -> bool:
        if self.state == "CLOSED":
            return True

        if self.state == "OPEN":
            now = time.time()
            elapsed = now - self.last_failure_time

            if elapsed > config.CIRCUIT_BREAKER_RESET_TIMEOUT:
                logger.info("Circuit breaker reset.")
                self.state = "CLOSED"
                self.failure_count = 0
                return True

            raise CircuitBreakerOpen(
                "Circuit breaker is open. Requests blocked."
            )

        return False
