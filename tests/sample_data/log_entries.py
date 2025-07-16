# Sample log entries to use in tests
PARSED_SAMPLE_LOGS = [
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


RAW_SAMPLE_LOGS = [
    "2025-07-05 14:06:09,890 [INFO] : Message A",
    "2025-07-05 14:07:09,890 [ERROR] : Message B",
    "2025-07-06 14:46:09,890 [DEBUG] : Message C",
    "2025-07-06 15:24:09,890 [INFO] : Message D"
]
