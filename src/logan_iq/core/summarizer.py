from typing import List, Dict
from collections import defaultdict

from .utils.date import parse_date


class LogSummarizer:
    """Summarize parsed logs: count levels, logs per day, etc."""

    def count_levels(self, logs: List[dict]) -> Dict[str, int]:
        """
        Count the number of entries per log level (case-insensitive).
        Missing levels are counted as 'UNKNOWN'.
        """
        counts = defaultdict(int)

        for log in logs:
            level = log.get("level", "").upper()
            counts[level if level else "UNKNOWN"] += 1

        return dict(counts)

    def count_logs_in_a_day(
        self,
        logs: List[dict],
        day: str,
        day_fmt: str = "%Y-%m-%d",
        log_fmt: str = "%Y-%m-%d %H:%M:%S,%f",
    ) -> Dict[str, int]:
        """
        Count logs grouped by level for a specific day.

        Args:
            logs: List of parsed log dicts
            day: Day string (YYYY-MM-DD by default)
            day_fmt: Format of the input day string
            log_fmt: Format of the datetime in log entries
        """
        day_dt = parse_date(day, day_fmt)
        if not day_dt:
            raise ValueError(f"Invalid day: {day}")

        counts = defaultdict(int)
        for log in logs:
            log_dt = parse_date(log.get("datetime"), log_fmt)
            if log_dt and log_dt.date() == day_dt.date():
                level = log.get("level", "").upper() or "UNKNOWN"
                counts[level] += 1

        return dict(counts)