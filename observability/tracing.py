"""
Tracing utilities for agent execution.
"""

import uuid
import time
from typing import Dict, Any, List

from observability.logger import logger


class Trace:
    """
    Represents a single agent execution trace.
    """

    def __init__(self) -> None:
        self.run_id = str(uuid.uuid4())
        self.start_time = time.time()
        self.steps: List[Dict[str, Any]] = []

        logger.info("Trace started | run_id=%s", self.run_id)

    def record_step(
        self,
        step_type: str,
        data: Dict[str, Any],
    ) -> None:
        """
        Record a trace step.
        """
        self.steps.append(
            {
                "timestamp": time.time(),
                "type": step_type,
                "data": data,
            }
        )

        logger.info(
            "Trace step | run_id=%s | type=%s",
            self.run_id,
            step_type,
        )

    def end(self) -> Dict[str, Any]:
        """
        Finalize trace and return summary.
        """
        duration = time.time() - self.start_time

        summary = {
            "run_id": self.run_id,
            "duration_seconds": round(duration, 4),
            "total_steps": len(self.steps),
        }

        logger.info(
            "Trace ended | run_id=%s | duration=%.2fs",
            self.run_id,
            duration,
        )

        return summary
