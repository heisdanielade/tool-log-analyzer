from typing import List, Optional

from .utils.date import parse_date, DEFAULT_DATETIME_FORMAT


class LogFilter:
    """
    Filter parsed log entries by level, date range, and limit.
    """

    def __init__(self, datetime_format: str = DEFAULT_DATETIME_FORMAT):
        self.datetime_format = datetime_format

    def filter_by_level(self, logs: List[dict], level: str) -> List[dict]:
        """Return logs matching a given level (case-insensitive)."""
        return [log for log in logs if log.get("level", "").lower() == level.lower()]

    def filter_by_date_range(self, logs: List[dict], start: str, end: str) -> List[dict]:
        """
        Return logs whose datetime is within [start, end].
        Accepts full datetime or date-only strings.
        """
        # Parse start
        start_dt = parse_date(start, DEFAULT_DATETIME_FORMAT)
        if not start_dt and len(start) == 10:  # date-only
            start_dt = parse_date(start, "%Y-%m-%d")
            start_dt = start_dt.replace(hour=0, minute=0, second=0, microsecond=0)

        # Parse end
        end_dt = parse_date(end, DEFAULT_DATETIME_FORMAT)
        if not end_dt and len(end) == 10:  # date-only
            end_dt = parse_date(end, "%Y-%m-%d")
            end_dt = end_dt.replace(hour=23, minute=59, second=59, microsecond=999999)

        if not start_dt or not end_dt:
            raise ValueError(f"Invalid start or end date: {start} to {end}")

        filtered = []
        for log in logs:
            dt_str = log.get("datetime")
            if not dt_str:
                continue
            log_dt = parse_date(dt_str, DEFAULT_DATETIME_FORMAT)
            if log_dt and start_dt <= log_dt <= end_dt:
                filtered.append(log)

        return filtered

    def filter_by_keyword(self, logs: List[dict], keyword: str, parse_fmt: str) -> List[dict]:
        """Return logs where the message and/or (method, path, status_code) contains the keyword (case-insensitive)."""
        if not keyword:
            return logs

        keyword = keyword.lower()
        keys_to_check =  ("message", "path", "method", "status", "status_code")

        normalize = lambda v: str(v).lower() if v is not None else ""

        if parse_fmt == "json":
            return [
                log for log in logs
                if any(keyword in normalize(log.get(k)) for k in keys_to_check)
            ]
        else:
            return [
                log for log in logs
                if keyword in normalize(log.get("message"))
            ]

    def filter(
        self,
        logs: List[dict],
        level: Optional[str] = None,
        limit: Optional[int] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> List[dict]:
        """Apply level and/or date filters, then limit the results."""
        result = logs

        if level:
            result = self.filter_by_level(result, level)

        if start and end:
            result = self.filter_by_date_range(result, start, end)

        if limit is not None and limit > 0:
            result = result[:limit]

        return result
