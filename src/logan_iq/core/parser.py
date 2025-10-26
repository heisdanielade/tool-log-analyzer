import json
import re
from typing import List, Optional, Set


class LogParser:
    """Convert raw log lines into structured dictionaries using a selected regex profile or JSON format."""

    # Required fields for JSON format
    REQUIRED_JSON_FIELDS: Set[str] = {"datetime", "level"}

    # Predefined formats and their regex patterns
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
        "json": None,  # Special case handled in parse_line
    }

    def __init__(self, format_name: str = "simple", custom_regex: Optional[str] = None):
        """
        Args:
            format_name: Name of a predefined format OR "custom".
            custom_regex: Raw regex string if using a custom format.
        """
        if format_name == "custom":
            if not custom_regex:
                raise ValueError("Custom format selected but no regex provided")
            try:
                self.pattern = re.compile(custom_regex)
                self.format_name = format_name
            except re.error as e:
                raise ValueError(f"Invalid custom regex provided: {e}") from e
        else:
            if format_name not in self.AVAILABLE_FORMATS:
                raise ValueError(
                    f"Unsupported format: '{format_name}'. Supported: {list(self.AVAILABLE_FORMATS.keys())}"
                )
            self.format_name = format_name
            if format_name != "json":
                self.pattern = re.compile(self.AVAILABLE_FORMATS[format_name])

    def _parse_json_line(self, line: str) -> Optional[dict]:
        """
        Parse a JSON format log line.

        Args:
            line: A string containing a JSON object

        Returns:
            dict if valid JSON with required fields, otherwise None
        """
        try:
            data = json.loads(line)
            if not isinstance(data, dict):
                return None

            # Check for required fields
            if not all(field in data for field in self.REQUIRED_JSON_FIELDS):
                return None

            return data
        except json.JSONDecodeError:
            return None

    def parse_line(self, line: str) -> Optional[dict]:
        """
        Parse a single log line.
        Returns a dict if matched, otherwise None.
        """
        if self.format_name == "json":
            return self._parse_json_line(line)

        match = self.pattern.match(line)
        return match.groupdict() if match else None

    def parse_file(self, path: str) -> List[dict]:
        """
        Parse all lines in a file.
        Returns a list of parsed entries.
        Skips lines that don't match.

        For JSON format:
        - Expects one JSON object per line
        - Each line must be a valid JSON object with required fields
        """
        parsed_entries = []
        try:
            with open(path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parsed = self.parse_line(line)
                    if parsed:
                        parsed_entries.append(parsed)
        except FileNotFoundError:
            print(f"No such file or directory: {path}")
        except IOError as e:
            print(f"[ERROR] IO error occurred: {e}")
        except UnicodeDecodeError as e:
            print(f"[ERROR] File encoding error: {e}")

        return parsed_entries
