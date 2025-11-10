import os
import json
import re
import pytest
from pathlib import Path
from ..logan_iq.core.parser import LogParser
from .sample_data.log_entries import RAW_SAMPLE_LOGS


@pytest.fixture
def log_parser() -> LogParser:
    return LogParser()


@pytest.fixture
def json_parser() -> LogParser:
    return LogParser(format_name="json")


def test_parse_line_success_with_simple_format(log_parser):
    line = RAW_SAMPLE_LOGS[2]
    result = log_parser.parse_line(line)
    assert isinstance(result, dict)
    assert result["datetime"] == "2025-07-06 14:46:09,890"
    assert result["level"] == "DEBUG"
    assert result["message"] == "Message C"


def test_parse_invalid_line_returns_none(log_parser):
    bad_line = "INFO This is a bad line."
    assert log_parser.parse_line(bad_line) is None


def test_parse_empty_line_returns_none(log_parser):
    assert log_parser.parse_line("") is None


def test_parse_file_success(log_parser):
    file_path = os.path.join(os.path.dirname(__file__), "sample_data", "raw_log_file.log")
    results = log_parser.parse_file(file_path)
    assert isinstance(results, list)
    assert len(results) == 4
    assert results[0]["level"] == "DEBUG"


def test_parse_file_not_found(log_parser, capsys):
    results = log_parser.parse_file("nonexistent.log")
    captured = capsys.readouterr()
    assert "File not found" in captured.out or "IO error" in captured.out
    assert results == []


def test_unsupported_format_raises_valueerror():
    with pytest.raises(ValueError):
        LogParser("unsupported")


def test_custom_regex_valid_and_invalid():
    valid_regex = r"^(?P<level>\w+): (?P<message>.+)$"
    parser = LogParser(format_name="custom", custom_regex=valid_regex)
    result = parser.parse_line("INFO: Test message")
    assert result["level"] == "INFO"
    assert result["message"] == "Test message"

    with pytest.raises(ValueError):
        LogParser(format_name="custom")  # No regex provided

    with pytest.raises(ValueError):
        LogParser(format_name="custom", custom_regex="(")  # Invalid regex


# JSON format tests
def test_parse_valid_json_line(json_parser):
    log_line = json.dumps({
        "datetime": "2025-10-26 12:34:56",
        "level": "INFO",
        "message": "Test",
        "extra": "value"
    })
    parsed = json_parser.parse_line(log_line)
    assert parsed["datetime"] == "2025-10-26 12:34:56"
    assert parsed["level"] == "INFO"
    assert parsed["message"] == "Test"
    assert parsed["extra"] == "value"


def test_parse_invalid_json_returns_none(json_parser):
    invalid_json = "{invalid}"
    assert json_parser.parse_line(invalid_json) is None


def test_parse_json_missing_required_fields(json_parser):
    log_line = json.dumps({"message": "No datetime or level"})
    assert json_parser.parse_line(log_line) is None


def test_parse_json_file(tmp_path: Path, json_parser):
    log_entries = [
        {"datetime": "2025-10-26 12:34:56", "level": "INFO", "message": "One"},
        {"datetime": "2025-10-26 12:34:57", "level": "ERROR", "message": "Two"}
    ]
    file_path = tmp_path / "logs.json"
    file_path.write_text("\n".join(json.dumps(e) for e in log_entries), encoding="utf-8")

    results = json_parser.parse_file(str(file_path))
    assert len(results) == 2
    assert results[0]["message"] == "One"
    assert results[1]["level"] == "ERROR"


def test_parse_json_with_extra_fields(json_parser):
    log_line = json.dumps({
        "datetime": "2025-10-26 12:34:56",
        "level": "INFO",
        "message": "Test",
        "extra": "field"
    })
    parsed = json_parser.parse_line(log_line)
    assert parsed.get("extra") == "field"
