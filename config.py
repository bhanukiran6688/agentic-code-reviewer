"""
Global configuration for the Agentic Code Reviewer.
"""

from pathlib import Path


# =========================
# LLM Configuration
# =========================
MODEL_NAME = "gemini-2.5-flash"
TEMPERATURE = 0.2
MAX_TOKENS = 1500

# Pricing (adjust if needed)
COST_PER_1K_INPUT_TOKENS = 0.0005
COST_PER_1K_OUTPUT_TOKENS = 0.0015


# =========================
# Reliability Configuration
# =========================
MAX_RETRIES = 3
RETRY_BACKOFF_SECONDS = 2

RATE_LIMIT_REQUESTS_PER_MINUTE = 20

CIRCUIT_BREAKER_FAILURE_THRESHOLD = 5
CIRCUIT_BREAKER_RESET_TIMEOUT = 60  # seconds


# =========================
# Agent Configuration
# =========================
MAX_AGENT_ITERATIONS = 8


# =========================
# Storage Paths
# =========================
BASE_DIR = Path(__file__).parent

STORAGE_DIR = BASE_DIR / "storage"
REPORTS_DIR = STORAGE_DIR / "reports"
PROMPT_VERSION_FILE = STORAGE_DIR / "prompt_versions.json"
METRICS_DB_PATH = STORAGE_DIR / "metrics.db"

STORAGE_DIR.mkdir(exist_ok=True)
REPORTS_DIR.mkdir(exist_ok=True)
