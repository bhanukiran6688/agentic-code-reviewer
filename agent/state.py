"""
Agent state tracking.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Any


@dataclass
class AgentState:
    """
    Tracks conversation state for agent loop.
    """

    messages: List[Dict[str, Any]] = field(default_factory=list)
    iteration_count: int = 0
    done: bool = False
    final_output: str | None = None

    def add_message(self, role: str, content: str) -> None:
        self.messages.append(
            {
                "role": role,
                "content": content,
            }
        )

    def increment_iteration(self) -> None:
        self.iteration_count += 1

    def complete(self, output: str) -> None:
        self.done = True
        self.final_output = output
