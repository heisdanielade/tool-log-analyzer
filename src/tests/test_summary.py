import pytest

from .sample_data.log_entries import PARSED_SAMPLE_LOGS

from logan_iq.core.summarizer import LogSummarizer


@pytest.fixture
def log_summary() -> LogSummarizer:
    """Log Summary istance for related tests"""
    return LogSummarizer()


def test_count_levels(log_summary):
    """
    Give counts of various log levels in all log entries.
    Tests count accuracy.
    """
    result = log_summary.count_levels(logs=PARSED_SAMPLE_LOGS)

    assert len(result) == 3
    assert result.get("INFO") == 3
    assert result.get("DEBUG") == 1
    assert result.get("ERROR") == 2