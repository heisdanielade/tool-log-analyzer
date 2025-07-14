from typing import List, Dict
from collections import defaultdict


class LogSummary:
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

    # TODO: Count logs per day/hour
    # TODO: Add pie chart with matplotlib
    # TODO: Output results to CSV
