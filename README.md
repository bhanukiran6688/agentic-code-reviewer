# Agentic Code Reviewer

A production-style, safety-aware Code Review Assistant that helps teams reduce PR review time and catch security/quality risks consistently.

This tool runs as a CLI (and is CI-friendly) to produce a structured review, risk annotations, and an auditable evaluation score, with reliability + safety guardrails.

This project demonstrates how to design and implement a complete agentic AI workflow including tool/function calling, iterative reasoning, safety guardrails, evaluation agents, observability, cost tracking, and reliability engineering patterns.

---

# Overview

Given a Python file, the agent performs the following steps:

1. Reads and analyzes the file.
2. Calls tools dynamically (file reader, linter, complexity analyzer).
3. Iteratively reasons over tool outputs.
4. Generates a structured code review.
5. Evaluates review quality using a secondary LLM pass.
6. Applies security-focused safety validation.
7. Tracks token usage, cost, and latency.
8. Persists metrics to SQLite.
9. Saves a Markdown report.

This system reflects real-world agentic AI orchestration patterns.

---

# Success criteria (measurable)
A run is considered successful when it:

- Flags high-severity issues (security, correctness) with specific file/line references
- Produces actionable recommendations (what to change + why)
- Avoids unsafe guidance (validated by safety checks)
- Completes within configured budgets (max iterations, token/cost limits)
- Produces reproducible artifacts (report + metrics + prompt version)

---

# Architecture

```
CLI (main.py)
   ↓
CodeReviewAgent
   ↓
GeminiClient (Resilience Layer)
   ↓
Tool Layer (Controlled Execution)
   ↓
Guardrails
   ↓
Evaluation Agent
   ↓
Safety Checks
   ↓
Tracing + Metrics Persistence
```

The architecture separates reasoning, execution, safety, evaluation, and observability into distinct layers.

---

# Project Structure

```
agentic-code-reviewer/
│
├── main.py
├── config.py
│
├── agent/
│   ├── orchestrator.py
│   ├── state.py
│   ├── prompts.py
│   ├── tools.py
│   ├── tool_registry.py
│   └── guardrails.py
│
├── llm/
│   ├── client.py
│   ├── retry.py
│   ├── rate_limiter.py
│   ├── circuit_breaker.py
│   └── cost_tracker.py
│
├── evaluation/
│   ├── quality_scoring.py
│   └── safety_checks.py
│
├── observability/
│   ├── logger.py
│   ├── tracing.py
│   └── metrics.py
│
├── storage/
│   ├── metrics.db
│   ├── prompt_versions.json
│   └── reports/
│
└── sample_code/
    └── bad_code_example.py
```

---

# Agentic AI features used
This project uses the following agentic features in its implementation:

## Core agent architecture
- Goal → Plan → Act → Observe → Repeat loop with termination limits
- State management (conversation/session state persisted during the run)

## Tooling & function calling
- Dynamic tool selection (file reader, linter, complexity analyzer, line counter)
- Tool chaining (tool outputs feed subsequent reasoning steps)
- Guarded tool execution + argument validation

## Planning & reasoning
- Plan-Act-Observe loop (iterative refinement)
- Critic-style evaluation via a secondary “Evaluation Agent” pass

## Observability & monitoring
- Run-level tracing (`run_id`), iteration/tool-call logging
- Token usage, latency, and cost tracking
- Metrics persistence (SQLite)

## Guardrails & safety
- Tool authorization + path restriction
- Prompt injection detection
- Output validation for unsafe patterns (e.g., `eval`, `os.system`, subprocess usage)
- Post-review security checks

---

# Core Concepts Demonstrated

## 1. Agentic AI Workflow

The system implements a full reasoning loop:

Goal → Plan → Act → Observe → Repeat

The agent:

* Maintains conversational state
* Dynamically selects tools
* Injects tool outputs back into reasoning
* Iterates with termination limits
* Produces a final structured output

This reflects real agentic systems used in production environments.

---

## 2. Tool / Function Calling

The LLM:

* Chooses a tool
* Provides structured arguments
* Receives structured tool output
* Continues reasoning based on results

Tools implemented:

* File reader
* Line counter
* Complexity analyzer (AST-based)
* Simple linter

Tool execution is guarded and validated.

---

## 3. Reliability Engineering for LLM Systems

The Gemini client is wrapped with:

* Rate limiting
* Retry with exponential backoff
* Circuit breaker
* Latency tracking
* Cost tracking

All model calls go through a resilience layer. No direct API calls bypass safety mechanisms.

---

## 4. Observability and Monitoring

### Structured Logging

Clear and consistent logs for every execution step.

### Tracing

Each run receives a unique `run_id`.
Tracks:

* Iterations
* Tool calls
* Execution duration

### Metrics Persistence (SQLite)

Stored in:

```
storage/metrics.db
```

Tracks:

* Run duration
* Iteration count
* Token usage
* Estimated cost
* Tool call frequency

This mirrors production AI observability patterns.

---

## 5. Cost and Token Monitoring

The system records:

* Input tokens
* Output tokens
* Estimated cost per call
* Total cost per run
* Average latency

Cost governance is critical in enterprise AI systems.

---

## 6. Guardrails and Safety

### Tool Authorization

Only registered tools may execute.

### Path Restriction

Prevents file system escape attempts.

### Prompt Injection Detection

Blocks attempts to override system instructions.

### Output Validation

Prevents unsafe patterns such as:

* eval()
* os.system
* subprocess execution

### Post-Review Security Checks

Detects insecure recommendations such as:

* Disabling authentication
* Removing validation
* Enabling unsafe debug modes

This enforces layered AI safety.

---

## 7. Evaluation Agent

After generating the review, a secondary LLM pass scores:

* Completeness
* Technical correctness
* Specificity
* Safety

This introduces multi-agent evaluation patterns commonly used in enterprise AI workflows.

---

## 8. Prompt Version Management

Prompts are stored in:

```
storage/prompt_versions.json
```

This enables:

* Prompt iteration
* Version tracking
* A/B testing
* Reproducibility
* Controlled experimentation

Production AI systems treat prompts as versioned assets.

---

# How to Run

## 1. Install Dependencies

```
pip install google-genai
```

## 2. Set Gemini API Key

Mac/Linux:

```
export GEMINI_API_KEY="your_api_key"
```

Windows:

```
setx GEMINI_API_KEY "your_api_key"
```

## 3. Execute

```
python main.py sample_code/bad_code_example.py
```

---

# Outputs Generated

After execution:

* Console output with review and evaluation
* Markdown report saved under `storage/reports/`
* Metrics stored in `storage/metrics.db`
* Prompt file created if not present

---

# Educational Value

This project provides hands-on exposure to:

* Agentic reasoning loops
* Tool orchestration
* LLM reliability engineering
* Safety and guardrail design
* Observability patterns
* Cost governance
* Evaluation agents
* Structured AI system architecture

The system is intentionally modular to reflect enterprise AI design principles.

---

# Summary

This repository demonstrates how to build a safe, observable, and production-oriented agentic AI system using Gemini.

It serves as a foundational blueprint for engineering enterprise-grade AI agents rather than simple prompt-based applications.
