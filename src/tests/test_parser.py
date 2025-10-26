import os
import json
import pytest
from pathlib import Path

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


@pytest.fixture
def json_parser() -> LogParser:
    """JSON Log Parser instance for all related tests."""
    return LogParser(format_name="json")


def test_json_format_initialization(json_parser):
    """
    Test that JSON format parser is initialized correctly with
    required fields configuration.
    """
    assert json_parser.format_name == "json"
    assert json_parser.REQUIRED_JSON_FIELDS == {"datetime", "level"}


def test_parse_valid_json_line(json_parser):
    """
    Test parsing a valid JSON log line with all required fields.
    Should return a dictionary with all fields preserved.
    """
    log_line = json.dumps(
        {
            "datetime": "2025-10-26 12:34:56",
            "level": "INFO",
            "message": "Request processed",
            "method": "GET",
            "status": 200,
            "path": "/api/v1/users",
        }
    )
    result = json_parser.parse_line(log_line)
    assert result is not None
    assert result["datetime"] == "2025-10-26 12:34:56"
    assert result["level"] == "INFO"
    assert result["message"] == "Request processed"
    assert result["method"] == "GET"
    assert result["status"] == 200
    assert result["path"] == "/api/v1/users"


def test_parse_invalid_json(json_parser):
    """
    Test parsing an invalid JSON string.
    Should return None.
    """
    invalid_json = "{invalid json}"
    result = json_parser.parse_line(invalid_json)
    assert result is None


def test_parse_json_missing_required_fields(json_parser):
    """
    Test parsing JSON without required fields (datetime, level).
    Should return None.
    """
    log_line = json.dumps(
        {
            "message": "Request processed",
            "method": "GET",
            "status": 200,
            "path": "/api/v1/users",
        }
    )
    result = json_parser.parse_line(log_line)
    assert result is None


def test_parse_json_file(tmp_path: Path, json_parser):
    """
    Test parsing a file containing JSON logs (one per line).
    Should return a list of parsed entries.
    """
    log_entries = [
        {
            "datetime": "2025-10-26 12:34:56",
            "level": "INFO",
            "message": "First request",
            "method": "GET",
            "status": 200,
            "path": "/api/v1/users",
        },
        {
            "datetime": "2025-10-26 12:34:57",
            "level": "ERROR",
            "message": "Second request failed",
            "method": "POST",
            "status": 500,
            "path": "/api/v1/users",
        },
    ]

    test_file = tmp_path / "test.json"
    with open(test_file, "w", encoding="utf-8") as f:
        for entry in log_entries:
            f.write(json.dumps(entry) + "\n")

    results = json_parser.parse_file(str(test_file))
    assert len(results) == 2
    assert results[0]["message"] == "First request"
    assert results[1]["message"] == "Second request failed"


def test_parse_json_with_extra_fields(json_parser):
    """
    Test parsing JSON with additional fields beyond the required ones.
    Should preserve all fields in the output.
    """
    log_line = json.dumps(
        {
            "datetime": "2025-10-26 12:34:56",
            "level": "INFO",
            "message": "Request processed",
            "method": "GET",
            "status": 200,
            "path": "/api/v1/users",
            "extra_field": "some value",
        }
    )
    result = json_parser.parse_line(log_line)
    assert result is not None
    assert "extra_field" in result
