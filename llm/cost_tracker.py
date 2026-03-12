"""
Tracks LLM usage cost and latency.
"""

from dataclasses import dataclass

from observability.logger import logger
import config


@dataclass
class CostTracker:
    """
    Tracks token usage and cost metrics.
    """

    input_tokens: int = 0
    output_tokens: int = 0
    total_cost: float = 0.0
    total_latency: float = 0.0
    calls: int = 0

    def record_call(
        self,
        input_tokens: int,
        output_tokens: int,
        latency_seconds: float,
    ) -> None:
        """
        Record a single LLM call usage.
        """
        self.input_tokens += input_tokens
        self.output_tokens += output_tokens
        self.calls += 1
        self.total_latency += latency_seconds

        input_cost = (
            input_tokens / 1000
        ) * config.COST_PER_1K_INPUT_TOKENS

        output_cost = (
            output_tokens / 1000
        ) * config.COST_PER_1K_OUTPUT_TOKENS

        self.total_cost += input_cost + output_cost

        logger.info(
            "LLM call | input_tokens=%s output_tokens=%s latency=%.2fs cost=%.6f",
            input_tokens,
            output_tokens,
            latency_seconds,
            input_cost + output_cost,
        )

    def summary(self) -> dict:
        """
        Return aggregated metrics.
        """
        avg_latency = (
            self.total_latency / self.calls
            if self.calls > 0
            else 0.0
        )

        return {
            "calls": self.calls,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_cost": round(self.total_cost, 6),
            "avg_latency_seconds": round(avg_latency, 4),
        }
