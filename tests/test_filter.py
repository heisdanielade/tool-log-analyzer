import pytest
from core.filter import LogFilter
from datetime import datetime


@pytest.fixture
def log_filter():
    return LogFilter()


# Sample log entries to use in tests
SAMPLE_LOGS = [
    {"datetime": "2025-07-05 14:06:09,890",
        "level": "INFO", "message": "Message A"},
    {"datetime": "2025-07-05 14:22:27,552",
        "level": "ERROR", "message": "Message B"},
    {"datetime": "2025-07-05 14:23:34,865",
        "level": "DEBUG", "message": "Message C"},
    {"datetime": "2025-07-06 15:00:00,000",
        "level": "INFO", "message": "Message D"},
    {"datetime": "2025-07-06 16:35:24,185",
        "level": "ERROR", "message": "Message E"},
    {"datetime": "2025-07-06 16:37:14,429",
        "level": "INFO", "message": "Message F"},
]


def test_filter_by_level(log_filter):
    """Filter parsed logs by DEBUG logs."""
    level = "DEBUG"
    result = log_filter.filter_by_level(SAMPLE_LOGS, level)
    assert len(result) == 1
    assert result[0]["level"] == level


def test_filter_by_date_range(log_filter):
    """Filter parsed logs by date range."""
    start = "2025-07-05 14:20:09,890"
    end = "2025-07-06 15:10:00,000"

    result = log_filter.filter_by_date_range(SAMPLE_LOGS, start, end)
    print(f"filter_by_date_range_result: {result}\n")

    assert len(result) > 0
    assert all(start <= log["datetime"] <= end for log in result)


def test_filter_by_limit(log_filter):
    """Filter on INFO logs but limit result dataset to 2."""
    result = log_filter.filter(SAMPLE_LOGS, level="INFO", limit=2)
    print(f"filter_by_limit_result: {result}\n")

    assert len(result) == 2
    assert result[1]["message"] == "Message D"


def test_filter_by_level_and_date_range(log_filter):
    """Filter only ERROR logs on a specific day."""
    level = "ERROR"
    start = "2025-07-06 00:00:00,000"
    end = "2025-07-06 23:59:59,999"

    result = log_filter.filter(SAMPLE_LOGS, level=level, start=start, end=end)
    print(f"filter_by_level_and_date_range_result: {result}\n")

    assert len(result) == 1
    assert result[0]["level"] == "ERROR"


def test_invalid_log_level(log_filter):
    """
    Filter by an invalid log level.
    Result set should be empty due invalid/incorrect log level.
    """
    level = "SIUUU"
    result = log_filter.filter(SAMPLE_LOGS, level=level)

    print(f"filter_by_invalid_level_result: {result}\n")
    assert len(result) == 0
