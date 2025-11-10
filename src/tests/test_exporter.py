import json
from pathlib import Path
from ..logan_iq.core.exporter import Exporter


def test_to_table_with_mixed_keys():
    exporter = Exporter()
    data = [
        {"datetime": "2025-10-26", "level": "INFO", "message": "ok", "method": "GET"},
        {
            "datetime": "2025-10-26",
            "level": "ERROR",
            "message": "fail",
            "status": 500,
            "path": "/api",
        },
    ]

    table = exporter.to_table(data)
    # Should include headers for keys from both records
    for key in ["datetime", "level", "message", "method", "status", "path"]:
        assert key in table
    # Ensure values are present
    for value in ["GET", "500", "/api"]:
        assert str(value) in table


def test_to_table_handles_missing_fields():
    exporter = Exporter()
    data = [
        {"a": 1, "b": 2},
        {"a": 3, "c": 4},
    ]
    table = exporter.to_table(data)
    for key in ["a", "b", "c"]:
        assert key in table
    for value in ["1", "3", "4"]:
        assert str(value) in table


def test_to_table_empty_returns_message():
    exporter = Exporter()
    assert exporter.to_table([]) == "No data to display."


def test_to_csv_creates_file(tmp_path):
    exporter = Exporter()
    data = [{"x": 1, "y": 2}, {"x": 3, "y": 4}]
    file_path = tmp_path / "output.csv"
    exporter.to_csv(data, str(file_path))

    # File should exist
    assert file_path.exists()
    content = file_path.read_text()
    for value in ["1", "2", "3", "4"]:
        assert str(value) in content


def test_to_csv_empty_data(tmp_path, capsys):
    exporter = Exporter()
    file_path = tmp_path / "empty.csv"
    exporter.to_csv([], str(file_path))
    # Should print message, file should not exist
    captured = capsys.readouterr()
    assert "No data to export." in captured.out
    assert not file_path.exists()


def test_to_json_creates_file(tmp_path):
    exporter = Exporter()
    data = [{"a": "foo", "b": "bar"}]
    file_path = tmp_path / "output.json"
    exporter.to_json(data, str(file_path))

    assert file_path.exists()
    loaded = json.loads(file_path.read_text())
    assert loaded == data
