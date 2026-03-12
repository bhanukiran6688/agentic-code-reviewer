"""
Gemini LLM client wrapper with:
- Rate limiting
- Retry logic
- Circuit breaker
- Cost tracking
- Latency monitoring
"""

import time
from google import genai
from google.genai import types

import config
from llm.rate_limiter import RateLimiter
from llm.retry import retry
from llm.circuit_breaker import CircuitBreaker, CircuitBreakerOpen
from llm.cost_tracker import CostTracker
from observability.logger import logger


class GeminiClient:
    """
    Wrapper around Gemini API with full reliability,
    tool-calling support, and cost tracking.
    """

    def __init__(self) -> None:
        self.client = genai.Client()
        self.rate_limiter = RateLimiter(
            max_requests=config.RATE_LIMIT_REQUESTS_PER_MINUTE
        )
        self.circuit_breaker = CircuitBreaker()
        self.cost_tracker = CostTracker()

    def _execute_call(
        self,
        contents,
        temperature: float,
        max_output_tokens: int,
        tools: list | None = None,
    ):
        """
        Internal execution wrapper with full resilience.
        """

        if not self.circuit_breaker.allow_request():
            raise CircuitBreakerOpen("Circuit breaker is open.")

        self.rate_limiter.acquire()

        def _call_model():
            start_time = time.time()

            response = self.client.models.generate_content(
                model=config.MODEL_NAME,
                contents=contents,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_output_tokens,
                    tools=tools,
                ),
            )

            latency = time.time() - start_time

            input_tokens = (
                response.usage_metadata.prompt_token_count
                if response.usage_metadata
                else 0
            )

            output_tokens = (
                response.usage_metadata.candidates_token_count
                if response.usage_metadata
                else 0
            )

            self.cost_tracker.record_call(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                latency_seconds=latency,
            )

            return response

        try:
            response = retry(
                _call_model,
                exceptions=Exception,
            )
            self.circuit_breaker.record_success()

        except Exception as exc:
            logger.error("Gemini call failed: %s", str(exc))
            self.circuit_breaker.record_failure()
            raise

        return response

    def generate(
        self,
        contents,
        temperature: float | None = None,
        max_output_tokens: int | None = None,
    ) -> str:
        """
        Standard text generation (no tools).
        """
        temperature = temperature or config.TEMPERATURE
        max_output_tokens = max_output_tokens or config.MAX_TOKENS

        response = self._execute_call(
            contents=contents,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
        )

        if not response.candidates:
            return ""

        return response.text

    def generate_with_tools(
        self,
        contents,
        tools: list,
        temperature: float | None = None,
        max_output_tokens: int | None = None,
    ):
        """
        Generation with tool-calling enabled.
        Returns full raw response.
        """
        temperature = temperature or config.TEMPERATURE
        max_output_tokens = max_output_tokens or config.MAX_TOKENS

        return self._execute_call(
            contents=contents,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            tools=tools,
        )

    def get_metrics(self):
        return self.cost_tracker.summary()

