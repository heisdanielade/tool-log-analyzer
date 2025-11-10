import pytest
from ..logan_iq.core.summarizer import LogSummarizer
from .sample_data.log_entries import PARSED_SAMPLE_LOGS

@pytest.fixture
def summarizer() -> LogSummarizer:
    return LogSummarizer()


def test_count_levels_basic(summarizer):
    """Count log levels in the sample logs."""
    result = summarizer.count_levels(PARSED_SAMPLE_LOGS)
    assert isinstance(result, dict)
    # Expect levels INFO, ERROR, DEBUG in sample
    assert result["INFO"] == 3
    assert result["ERROR"] == 2
    assert result["DEBUG"] == 1


def test_count_levels_with_missing_level(summarizer):
    """Logs without a level should be counted as 'UNKNOWN'."""
    logs = [
        {"datetime": "2025-07-05 12:00:00,000", "level": "INFO"},
        {"datetime": "2025-07-05 12:01:00,000"},
    ]
    result = summarizer.count_levels(logs)
    assert result["INFO"] == 1
    assert result["UNKNOWN"] == 1


def test_count_logs_in_a_day_valid_day(summarizer):
    """Count logs per level for a specific day."""
    day = "2025-07-05"
    result = summarizer.count_logs_in_a_day(PARSED_SAMPLE_LOGS, day)
    # On 2025-07-05 there are INFO=1, ERROR=1, DEBUG=1
    assert result == {"INFO": 1, "ERROR": 1, "DEBUG": 1}


def test_count_logs_in_a_day_another_day(summarizer):
    """Count logs for a day with multiple entries of the same level."""
    day = "2025-07-06"
    result = summarizer.count_logs_in_a_day(PARSED_SAMPLE_LOGS, day)
    # On 2025-07-06: INFO=2, ERROR=1
    assert result == {"INFO": 2, "ERROR": 1}


def test_count_logs_in_a_day_no_logs(summarizer):
    """Return empty dict if no logs exist on the day."""
    day = "2025-07-07"
    result = summarizer.count_logs_in_a_day(PARSED_SAMPLE_LOGS, day)
    assert result == {}


def test_count_logs_in_a_day_with_invalid_day(summarizer):
    """Should raise ValueError if day string is invalid."""
    with pytest.raises(ValueError):
        summarizer.count_logs_in_a_day(PARSED_SAMPLE_LOGS, "invalid-date")


def test_count_logs_in_a_day_missing_level(summarizer):
    """Logs without a level on a specific day should be counted as UNKNOWN."""
    logs = [
        {"datetime": "2025-07-06 10:00:00,000"},
        {"datetime": "2025-07-06 12:00:00,000", "level": "INFO"},
    ]
    result = summarizer.count_logs_in_a_day(logs, "2025-07-06")
    assert result["INFO"] == 1
    assert result["UNKNOWN"] == 1


def test_count_logs_in_a_day_custom_formats(summarizer):
    """Supports custom day and log datetime formats."""
    logs = [
        {"datetime": "07/06/2025 10:00:00", "level": "INFO"},
        {"datetime": "07/06/2025 12:00:00", "level": "ERROR"},
    ]
    day_fmt = "%m/%d/%Y"
    log_fmt = "%m/%d/%Y %H:%M:%S"
    result = summarizer.count_logs_in_a_day(logs, "07/06/2025", day_fmt=day_fmt, log_fmt=log_fmt)
    assert result == {"INFO": 1, "ERROR": 1}
