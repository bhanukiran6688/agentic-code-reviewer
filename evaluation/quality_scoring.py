"""
Evaluation module for scoring review quality.
"""

import json
from typing import Dict, Any

from llm.client import GeminiClient
from agent.prompts import load_prompts
from observability.logger import logger


class ReviewEvaluator:
    """
    Evaluates the quality of a generated review.
    """

    def __init__(self) -> None:
        self.llm = GeminiClient()
        self.prompts = load_prompts()

    def evaluate(self, review_text: str) -> Dict[str, Any]:
        """
        Score review quality using LLM.
        """
        system_prompt = self.prompts["evaluation_system_v1"]

        full_prompt = (
            f"{system_prompt}\n\n"
            f"Review to evaluate:\n{review_text}"
        )

        response_text = self.llm.generate(
            contents=full_prompt,
            temperature=0.0,
            max_output_tokens=300,
        )

        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            logger.warning("Evaluation response not valid JSON.")
            result = {
                "score": 0,
                "reason": "Invalid evaluation response format.",
            }

        return result
