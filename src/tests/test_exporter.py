from logan_iq.core.exporter import Exporter


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
    assert "datetime" in table
    assert "level" in table
    assert "message" in table
    assert "method" in table
    assert "status" in table
    assert "path" in table
    # Ensure values are present
    assert "GET" in table
    assert "500" in table
    assert "/api" in table


def test_to_table_handles_missing_fields():
    exporter = Exporter()
    data = [
        {"a": 1, "b": 2},
        {"a": 3, "c": 4},
    ]
    table = exporter.to_table(data)
    assert "a" in table
    assert "b" in table
    assert "c" in table
    assert "1" in table
    assert "3" in table
    assert "4" in table
