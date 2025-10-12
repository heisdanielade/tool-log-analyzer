import os

import pytest

from .sample_data.log_entries import RAW_SAMPLE_LOGS
from logan_iq.core.parser import LogParser


@pytest.fixture
def log_parser() -> LogParser:
    """Log Parser instance for all related tests."""
    return LogParser()


def test_parse_line_success_with_simple_format(log_parser):
    """
    Parse line correctly using default format (simple) and
    return a dictionary with parsed log entry.
    """
    line = RAW_SAMPLE_LOGS[2]
    result = log_parser.parse_line(line)

    expected_parsed_datetime = "2025-07-06 14:46:09,890"
    expected_parsed_level = "DEBUG"
    expected_parsed_message = "Message C"

    print(f"parse_line_success_result: {result}\n")

    assert isinstance(result, dict)
    assert result["datetime"] == expected_parsed_datetime
    assert result["level"] == expected_parsed_level
    assert result["message"] == expected_parsed_message


def test_parse_invalid_line_with_simple_format(log_parser):
    """
    Trying to parse an invalid line (unsupported format) using the
    simple format should return None.
    """
    bad_line = "INFO This is a bad line."
    result = log_parser.parse_line(bad_line)
    assert result is None


def test_parse_file_success_with_simple_format(
    log_parser, expected_result_count: int = 4
):
    """
    Parse file correctly using default format (simple) and
    return List containing dicts of parsed log entries.
    """
    file = os.path.join(os.path.dirname(__file__), "sample_data", "raw_log_file.log")
    result = log_parser.parse_file(file)

    print(f"parse_file_success_result: {result}\n")
    assert isinstance(result, list)
    assert len(result) == expected_result_count
    assert result[0]["level"] == "DEBUG"
    assert result[1]["message"] == "Info message."
    assert result[2]["datetime"] == "2025-07-05 14:23:34,865"


def test_parse_file_with_invalid_file_path(
    log_parser, capsys, expected_result_count: int = 0
):
    """
    Parse file correctly using default format (simple) and
    return List containing dicts of parsed log entries.
    """
    file = "Invalid file path"
    result = log_parser.parse_file(file)

    captured = capsys.readouterr()
    assert "No such file or directory" in captured.out
    assert len(result) == expected_result_count


def test_parse_with_unsupported_format():
    """
    Instantiating Log Parser with an unsupported format should
    raise a ValueError.
    """
    bad_format = "garbage"
    line = RAW_SAMPLE_LOGS[0]
    with pytest.raises(ValueError):
        LogParser(bad_format).parse_line(line)
