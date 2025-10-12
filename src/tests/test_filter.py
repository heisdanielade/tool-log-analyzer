import pytest

from .sample_data.log_entries import PARSED_SAMPLE_LOGS
from logan_iq.core.filter import LogFilter


@pytest.fixture
def log_filter() -> LogFilter:
    """Log filter instance for all related tests."""
    return LogFilter()


def test_filter_by_level(log_filter, expected_result_count: int = 1) -> None:
    """Filter parsed logs by DEBUG logs."""
    level = "DEBUG"
    result = log_filter.filter_by_level(PARSED_SAMPLE_LOGS, level)
    assert len(result) == expected_result_count
    assert result[0]["level"] == level


def test_filter_by_date_range(log_filter) -> None:
    """Filter parsed logs by date range."""
    start = "2025-07-05 14:20:09,890"
    end = "2025-07-06 15:10:00,000"

    result = log_filter.filter_by_date_range(PARSED_SAMPLE_LOGS, start, end)
    print(f"filter_by_date_range_result: {result}\n")

    assert len(result) > 0
    assert all(start <= log["datetime"] <= end for log in result)


def test_filter_by_limit(log_filter, expected_result_count: int = 2) -> None:
    """Filter on INFO logs but limit result dataset to 2."""
    result = log_filter.filter(PARSED_SAMPLE_LOGS, level="INFO", limit=2)
    print(f"filter_by_limit_result: {result}\n")

    assert len(result) == expected_result_count
    assert result[1]["message"] == "Message D"


def test_filter_by_level_and_date_range(log_filter, expected_result_count: int = 1) -> None:
    """Filter only ERROR logs on a specific day."""
    level = "ERROR"
    start = "2025-07-06 00:00:00,000"
    end = "2025-07-06 23:59:59,999"

    result = log_filter.filter(
        PARSED_SAMPLE_LOGS, level=level, start=start, end=end)
    print(f"filter_by_level_and_date_range_result: {result}\n")

    assert len(result) == expected_result_count
    assert result[0]["level"] == "ERROR"


def test_invalid_log_level(log_filter, expected_result_count: int = 0) -> None:
    """
    Filter by an invalid log level.
    Result set should be empty due invalid/incorrect log level.
    """
    level = "SIUUU"
    result = log_filter.filter(PARSED_SAMPLE_LOGS, level=level)

    print(f"filter_by_invalid_level_result: {result}\n")
    assert len(result) == expected_result_count
