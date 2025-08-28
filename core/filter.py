from typing import List, Optional
from datetime import datetime


class LogFilter:
    """
    Return a list of parsed log entries filtered based on log level and/or date range.
    """

    def __init__(self, datetime_format: str = "%Y-%m-%d %H:%M:%S,%f"):
        self.datetime_format = datetime_format

    def filter_by_level(self, logs: List[dict], level: str) -> List[dict]:
        """
        Returns logs where the 'level' field matches the given level (case-insensitive).
        """
        return [log for log in logs if log.get("level", "").lower() == level.lower()]

    def filter_by_date_range(
        self, logs: List[dict], start: str, end: str
    ) -> List[dict]:
        """
        Returns logs where the 'datetime' field is within the [start, end] range.
        Dates must be strings in the datetime format used.
        """
        try:
            start_date = datetime.strptime(start, self.datetime_format)
            end_date = datetime.strptime(end, self.datetime_format)
        except ValueError as e:
            raise ValueError(f"Invalid date format: {e}")

        filtered = []
        for log in logs:
            try:
                log_date = datetime.strptime(log["datetime"], self.datetime_format)
                if start_date <= log_date <= end_date:
                    filtered.append(log)
            except Exception:
                continue  # To skip bad datetime formats

        return filtered

    def filter(
        self,
        logs: List[dict],
        level: Optional[str] = None,
        limit: Optional[int] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> List[dict]:
        """Apply level and/or date filters. Returns filtered logs."""
        result = logs
        if level:
            result = self.filter_by_level(result, level)
        if start and end:
            result = self.filter_by_date_range(result, start, end)
        if limit is None:
            pass
        elif 0 < limit < len(result):
            result = result[:limit]
        elif limit == 00:
            result = result[0:]

        return result
