import re
from typing import List, Optional


class LogParser:
    """Convert raw log lines into structured dictionaries using a selected regex profile."""

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
                raise ValueError(f"Invalid custom regex provided: {e}")
        else:
            if format_name not in self.AVAILABLE_FORMATS:
                raise ValueError(
                    f"Unsupported format: '{format_name}'. Supported: {list(self.AVAILABLE_FORMATS.keys())}"
                )
            self.format_name = format_name
            self.pattern = re.compile(self.AVAILABLE_FORMATS[format_name])

    def parse_line(self, line: str) -> Optional[dict]:
        """
        Parse a single log line.
        Returns a dict if matched, otherwise None.
        """
        match = self.pattern.match(line)
        return match.groupdict() if match else None

    def parse_file(self, path: str) -> List[dict]:
        """
        Parse all lines in a file.
        Returns a list of parsed entries.
        Skips lines that don't match.
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
        except Exception as e:
            print(f"[ERROR] {e}")

        return parsed_entries
