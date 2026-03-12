"""
Production-grade agent orchestration loop.
"""

import json
from typing import Any

import config
from agent.state import AgentState
from agent.prompts import load_prompts
from agent.tool_registry import TOOLS_SCHEMA, execute_tool
from agent.guardrails import Guardrails, GuardrailViolation
from evaluation.safety_checks import SafetyChecker
from llm.client import GeminiClient
from observability.logger import logger
from observability.tracing import Trace
from observability.metrics import MetricsStore


class CodeReviewAgent:
    """
    Agent responsible for reviewing code using tools
    with full observability and safety enforcement.
    """

    def __init__(self) -> None:
        self.llm = GeminiClient()
        self.prompts = load_prompts()
        self.metrics_store = MetricsStore()

    def run(self, file_path: str) -> str:
        """
        Execute full agent lifecycle.
        """
        state = AgentState()
        trace = Trace()
        system_prompt = self.prompts["review_system_v1"]
        state.add_message(role="user", content=f"{system_prompt}\n\nReview file: {file_path}")
        trace.record_step("agent_start", {"file_path": file_path},)
        while not state.done:
            if state.iteration_count >= config.MAX_AGENT_ITERATIONS:
                logger.warning("Max iterations reached.")
                state.complete("Agent stopped due to iteration limit.")
                break

            state.increment_iteration()
            trace.record_step("iteration", {"iteration": state.iteration_count},)
            response = self._call_model(state)
            if self._is_tool_call(response):
                self._handle_tool_call(response, state, trace)
            else:
                output_text = response
                try:
                    Guardrails.validate_output(output_text)
                except GuardrailViolation as exc:
                    output_text = f"Output blocked by guardrails: {exc}"

                state.complete(output_text)

        trace_summary = trace.end()
        metrics = self.llm.get_metrics()
        total_tokens = (metrics["input_tokens"] + metrics["output_tokens"])
        self.metrics_store.record_run(
            run_id=trace_summary["run_id"],
            duration_seconds=trace_summary["duration_seconds"],
            iterations=state.iteration_count,
            total_cost=metrics["total_cost"],
            total_tokens=total_tokens
        )

        # Safety validation (post-review)
        safety_result = SafetyChecker.validate_review(state.final_output or "")
        if not safety_result["safe"]:
            logger.warning("Safety issues detected in review.")
            state.final_output += (
                "\n\n⚠ SAFETY WARNINGS:\n"
                + "\n".join(safety_result["issues"])
            )
        return state.final_output or ""
    
    def _call_model(self, state: AgentState):
        """
        Call Gemini through resilience layer with tools.
        """
        
        last_user_message = state.messages[-1]["content"]
        
        try:
            Guardrails.detect_prompt_injection(last_user_message)
        except GuardrailViolation as exc:
            logger.error("Prompt injection detected.")
            state.complete(f"Blocked: {exc}")
            return ""
        
        response = self.llm.generate_with_tools(
            contents=state.messages,
            tools=TOOLS_SCHEMA,
        )
        
        if not response.candidates:
            return ""
        
        candidate = response.candidates[0]
        
        if not candidate.content.parts:
            return ""
        
        part = candidate.content.parts[0]
        
        if hasattr(part, "function_call"):
            return response
        
        return response.text
    
    @staticmethod
    def _is_tool_call(response: Any) -> bool:
        """
        Check if Gemini returned a tool call.
        """
        if not response:
            return False

        if hasattr(response, "candidates"):
            candidate = response.candidates[0]
            if candidate.content.parts:
                part = candidate.content.parts[0]
                return hasattr(part, "function_call")

        return False

    def _handle_tool_call(
        self,
        response: Any,
        state: AgentState,
        trace: Trace,
    ) -> None:
        """
        Execute tool safely and record metrics.
        """
        part = response.candidates[0].content.parts[0]
        function_call = part.function_call

        tool_name = function_call.name
        arguments = dict(function_call.args)

        try:
            Guardrails.validate_tool_call(tool_name, arguments)
        except GuardrailViolation as exc:
            state.add_message(
                role="assistant",
                content=f"Tool call blocked: {exc}",
            )
            return

        logger.info("Executing tool: %s", tool_name)

        trace.record_step(
            "tool_call",
            {"tool": tool_name, "arguments": arguments},
        )

        self.metrics_store.record_tool_call(
            run_id=trace.run_id,
            tool_name=tool_name,
        )

        try:
            result = execute_tool(tool_name, arguments)
        except Exception as exc:
            result = {
                "status": "error",
                "message": str(exc),
            }

        state.add_message(
            role="tool",
            content=json.dumps(
                {
                    "tool_name": tool_name,
                    "result": result,
                }
            ),
        )
