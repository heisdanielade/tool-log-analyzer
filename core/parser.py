import re
from typing import List, Optional


class LogParser:
    """Convert raw log lines into structured dictionaries using a selected regex profile."""

    # Predefined formats and their regex patterns
    available_formats = {
        "simple": r"^(?P<datetime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(?:,\d+)?) - (?P<level>\w+) - (?P<message>.+)$",
        "apache": r'^(?P<ip>\S+) - - \[(?P<datetime>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) \S+" (?P<status>\d+) \d+$',
    }

    def __init__(self, format_name: str = "simple"):
        if format_name not in self.available_formats:
            raise ValueError(
                f"Unsupported format: '{format_name}'. Supported: {list(self.available_formats.keys())}")
        self.format_name = format_name
        self.pattern = re.compile(self.available_formats[format_name])

    def parse_line(self, line: str) -> Optional[dict]:
        """
        Parse a single log line.
        Returns a dict if matched, otherwise None.
        """
        match = self.pattern.match(line)
        if match:
            return match.groupdict()
        return None

    def parse_file(self, path: str) -> List[dict]:
        """
        Parse all lines in a file.
        Returns a list of parsed entries.
        Skips lines that don't match.
        """
        parsed_entries = []
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parsed = self.parse_line(line)
                if parsed:
                    parsed_entries.append(parsed)
        return parsed_entries
