import json
import re
from typing import List, Optional, Set

class LogParser:
    """
    Convert raw log lines into structured dictionaries using a selected regex profile or JSON format.
    """

    # Required fields for JSON format
    REQUIRED_JSON_FIELDS: Set[str] = {"datetime", "level"}

    # Predefined formats
    AVAILABLE_FORMATS = {
        "simple": r"^(?P<datetime>.*?) \[(?P<level>\w+)\] .*?: (?P<message>.*)$",
        "apache": r'^(?P<ip>\S+) - - \[(?P<datetime>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) \S+" (?P<status>\d+) \d+$',
        "nginx": (
            r"^(?P<ip>\S+) - (?P<user>\S+) "
            r"\[(?P<datetime>[^\]]+)\] "
            r'"(?P<method>\S+) (?P<path>\S+) (?P<protocol>[^"]+)" '
            r"(?P<status>\d+) (?P<size>\d+) "
            r'"(?P<referer>[^"]*)" '
            r'"(?P<agent>[^"]*)"'
        ),
        "json": None,  # Special handling
    }

    def __init__(self, format_name: str = "simple", custom_regex: Optional[str] = None):
        """
        Args:
            format_name: predefined format or "custom"
            custom_regex: raw regex if using custom format
        """
        self.format_name = format_name.lower()

        if self.format_name == "custom":
            if not custom_regex:
                raise ValueError("Custom format selected but no regex provided")
            try:
                self.pattern = re.compile(custom_regex)
            except re.error as e:
                raise ValueError(f"Invalid custom regex provided: {e}") from e
        elif self.format_name in self.AVAILABLE_FORMATS:
            if self.format_name != "json":
                self.pattern = re.compile(self.AVAILABLE_FORMATS[self.format_name])
        else:
            raise ValueError(
                f"Unsupported format '{format_name}'. Supported: {list(self.AVAILABLE_FORMATS.keys()) + ['custom']}"
            )

    def _parse_json_line(self, line: str) -> Optional[dict]:
        """Parse a JSON log line; returns dict if valid, else None."""
        try:
            data = json.loads(line)
            if not isinstance(data, dict):
                return None
            if not all(field in data for field in self.REQUIRED_JSON_FIELDS):
                return None
            return data
        except json.JSONDecodeError:
            return None

    def parse_line(self, line: str) -> Optional[dict]:
        """Parse a single log line and return a dict if successful."""
        line = line.strip()
        if not line:
            return None

        if self.format_name == "json":
            return self._parse_json_line(line)

        match = self.pattern.match(line)
        return match.groupdict() if match else None

    def parse_file(self, path: str) -> List[dict]:
        """Parse all lines in a file and return a list of dicts."""
        parsed_entries: List[dict] = []

        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    parsed = self.parse_line(line)
                    if parsed:
                        parsed_entries.append(parsed)
        except FileNotFoundError:
            print(f"[ERROR] File not found: {path}")
        except IOError as e:
            print(f"[ERROR] IO error: {e}")
        except UnicodeDecodeError as e:
            print(f"[ERROR] File encoding error: {e}")

        return parsed_entries
