import pytest
from ..logan_iq.core.filter import LogFilter
from .sample_data.log_entries import PARSED_SAMPLE_LOGS


@pytest.fixture
def log_filter() -> LogFilter:
    return LogFilter()


def test_filter_by_level(log_filter):
    result = log_filter.filter_by_level(PARSED_SAMPLE_LOGS, "DEBUG")
    assert len(result) == 1
    assert result[0]["level"] == "DEBUG"


def test_filter_by_date_range(log_filter):
    start = "2025-07-05 14:06:09,890"
    end = "2025-07-06 16:35:24,185"
    result = log_filter.filter_by_date_range(PARSED_SAMPLE_LOGS, start, end)
    assert all(start <= log["datetime"] <= end for log in result)
    assert len(result) == 5


def test_filter_by_date_only_start_end(log_filter):
    """Test filtering with only a date (no time) should cover a full day."""
    start = "2025-07-06"
    end = "2025-07-06"
    result = log_filter.filter_by_date_range(PARSED_SAMPLE_LOGS, start, end)
    for log in result:
        assert log["datetime"].startswith("2025-07-06")
    assert len(result) > 0


def test_filter_with_limit(log_filter):
    result = log_filter.filter(PARSED_SAMPLE_LOGS, level="INFO", limit=2)
    assert len(result) == 2
    assert all(log["level"] == "INFO" for log in result)


def test_filter_by_level_and_date_range(log_filter):
    start = "2025-07-05 14:06:09,890"
    end = "2025-07-06 16:35:24,185"
    result = log_filter.filter(PARSED_SAMPLE_LOGS, level="ERROR", start=start, end=end)
    assert len(result) == 2
    assert result[0]["level"] == "ERROR"


def test_filter_invalid_level(log_filter):
    result = log_filter.filter(PARSED_SAMPLE_LOGS, level="SMILE")
    assert len(result) == 0


def test_filter_invalid_date_range_raises(log_filter):
    with pytest.raises(ValueError):
        log_filter.filter(PARSED_SAMPLE_LOGS, start="bad", end="2025-07-06")


def test_filter_empty_logs(log_filter):
    result = log_filter.filter([], level="INFO", start="2025-07-06", end="2025-07-06")
    assert result == []
