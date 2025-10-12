from typing import List, Dict
from collections import defaultdict
from datetime import datetime


class LogSummarizer:
    """Takes a list of parsed logs and returns summary statistics."""

    def count_levels(self, logs: List[dict]) -> Dict[str, int]:
        """
        Count the number of entries per log level.
        Returns a dictionary: {"INFO": 12, "ERROR" 5, ...},
            "UNKNOWN" for log entries without levels.
        Case insensitive i.e. 'error' and 'ERROR' are treated the same.
        """
        counts = defaultdict(int)

        for log in logs:
            level = log.get("level", "").upper()
            if level:
                counts[level] += 1
            else:
                counts["UNKNOWN"] += 1

        return dict(counts)

    def count_logs_in_a_day(self, logs: List[dict], day: datetime) -> Dict[str, int]:
        # TODO: Count logs per day/hour
        """ """
        counts = defaultdict(int)

        for log in logs:
            period = log.get("datetime", "")

        return None

    # TODO: Add pie chart with matplotlib
    # TODO: Output results to CSV
