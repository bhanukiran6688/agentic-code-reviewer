"""
Simple token bucket rate limiter.
"""

import threading
import time


class RateLimiter:
    """
    Token bucket rate limiter.

    Allows up to `max_requests` per `per_seconds`.
    """

    def __init__(self, max_requests: int, per_seconds: int = 60):
        self.max_requests = max_requests
        self.per_seconds = per_seconds
        self.tokens = max_requests
        self.lock = threading.Lock()
        self.last_refill = time.time()

    def _refill(self) -> None:
        now = time.time()
        elapsed = now - self.last_refill

        if elapsed > self.per_seconds:
            self.tokens = self.max_requests
            self.last_refill = now

    def acquire(self) -> None:
        """
        Blocks until a token is available.
        """
        while True:
            with self.lock:
                self._refill()

                if self.tokens > 0:
                    self.tokens -= 1
                    return

            time.sleep(0.1)
