"""
Entry point for Agentic Code Reviewer.
"""

import sys
import json
from pathlib import Path
from datetime import datetime, UTC

import config
from observability.logger import logger
from agent.orchestrator import CodeReviewAgent
from evaluation.quality_scoring import ReviewEvaluator


def save_report(file_path: str, review: str, evaluation: dict) -> None:
    """
    Save markdown report.
    """
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    report_file = (config.REPORTS_DIR / f"review_{Path(file_path).stem}_{timestamp}.md")
    content = (
        f"# Code Review Report\n\n"
        f"## File\n{file_path}\n\n"
        f"## Review\n{review}\n\n"
        f"## Evaluation\n"
        f"Score: {evaluation.get('score')}\n\n"
        f"Reason: {evaluation.get('reason')}\n"
    )
    report_file.write_text(content, encoding="utf-8")
    logger.info("Report saved to %s", report_file)


def main() -> None:
    """
    CLI entry.
    """
    if len(sys.argv) != 2:
        # python main.py sample_code/bad_code_example.py
        print("Usage: python main.py <file_path>")
        sys.exit(1)

    file_path = sys.argv[1]
    agent = CodeReviewAgent()
    evaluator = ReviewEvaluator()
    logger.info("Starting code review for %s", file_path)
    review_output = agent.run(file_path)
    logger.info("Running evaluation phase")
    evaluation_result = evaluator.evaluate(review_output)
    print("\n===== REVIEW OUTPUT =====\n")
    print(review_output)
    print("\n===== EVALUATION =====\n")
    print(json.dumps(evaluation_result, indent=2))
    metrics = agent.llm.get_metrics()
    print("\n===== LLM METRICS =====\n")
    print(json.dumps(metrics, indent=2))
    save_report(
        file_path=file_path,
        review=review_output,
        evaluation=evaluation_result
    )


if __name__ == "__main__":
    main()
