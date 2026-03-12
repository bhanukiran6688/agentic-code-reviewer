"""
Metrics persistence layer using SQLite.
"""

import time
import sqlite3

import config
from observability.logger import logger


class MetricsStore:
    """
    Stores agent run metrics in SQLite.
    """

    def __init__(self) -> None:
        self.conn = sqlite3.connect(config.METRICS_DB_PATH)
        self._create_tables()

    def _create_tables(self) -> None:
        cursor = self.conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS runs (
                run_id TEXT PRIMARY KEY,
                start_time REAL,
                duration_seconds REAL,
                iterations INTEGER,
                total_cost REAL,
                total_tokens INTEGER
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tool_calls (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                run_id TEXT,
                tool_name TEXT,
                timestamp REAL
            )
            """
        )

        self.conn.commit()

    def record_run(
        self,
        run_id: str,
        duration_seconds: float,
        iterations: int,
        total_cost: float,
        total_tokens: int,
    ) -> None:
        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT OR REPLACE INTO runs
            (run_id, start_time, duration_seconds,
             iterations, total_cost, total_tokens)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                run_id,
                time.time(),
                duration_seconds,
                iterations,
                total_cost,
                total_tokens,
            ),
        )

        self.conn.commit()

        logger.info("Metrics: Run recorded | run_id=%s", run_id)

    def record_tool_call(
        self,
        run_id: str,
        tool_name: str,
    ) -> None:
        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO tool_calls (run_id, tool_name, timestamp)
            VALUES (?, ?, ?)
            """,
            (run_id, tool_name, time.time()),
        )

        self.conn.commit()

        logger.info(
            "Metrics: Tool call recorded | run_id=%s | tool=%s",
            run_id,
            tool_name,
        )
