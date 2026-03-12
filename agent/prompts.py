"""
Prompt definitions and version management.
"""

import json
from typing import Dict

import config


DEFAULT_PROMPTS = {
    "review_system_v1": """
You are a senior Python code reviewer.

Your goals:
1. Understand the code.
2. Identify structural issues.
3. Identify complexity concerns.
4. Identify linting problems.
5. Suggest improvements.

You may call tools when needed.

Do not hallucinate file contents.
Only use tool outputs.
""",
    "evaluation_system_v1": """
You are a strict evaluator.

Score the quality of the review from 1-10 based on:
- Completeness
- Technical correctness
- Specificity
- Safety

Return JSON:
{
  "score": int,
  "reason": string
}
"""
}


def load_prompts() -> Dict[str, str]:
    """
    Load prompts from JSON file if exists,
    otherwise use defaults.
    """
    if config.PROMPT_VERSION_FILE.exists():
        return json.loads(config.PROMPT_VERSION_FILE.read_text(encoding="utf-8"))

    config.PROMPT_VERSION_FILE.write_text(json.dumps(DEFAULT_PROMPTS, indent=2), encoding="utf-8")
    return DEFAULT_PROMPTS
