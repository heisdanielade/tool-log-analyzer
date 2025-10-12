import os
from typing import List, Dict, Optional
from colorama import init, Fore

from .parser import LogParser
from .filter import LogFilter
from .summarizer import LogSummarizer
from .exporter import Exporter

init(autoreset=True)


class LogAnalyzer:
    """Analyzer class to associate CLI commands with log analysis features."""

    def __init__(self, parse_format: str, custom_regex: Optional[str] = None):
        """
        Initialize analyzer with a given format or custom regex.
        No default "simple" is hard-coded; the CLI or config should supply this.
        """
        self.parser = LogParser(parse_format, custom_regex=custom_regex)
        self.filter = LogFilter()
        self.summary = LogSummarizer()
        self.exporter = Exporter()

    def handle_invalid_file_path(self, file: str) -> None:
        """Handle FileNotFoundError if file path doesn't exist."""
        if file and not os.path.exists(file):
            print(Fore.RED + f"No such file or directory: {file}")
            exit(1)

    def analyze(self, file_path: str) -> List[dict]:
        """Parse entire log file."""
        self.handle_invalid_file_path(file_path)
        return self.parser.parse_file(file_path)  # type: ignore

    def filter_logs(
        self,
        file_path: str,
        level: Optional[str] = None,
        limit: Optional[int] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> List[dict]:
        """Parse and filter logs."""
        self.handle_invalid_file_path(file_path)
        logs = self.analyze(file_path)
        return self.filter.filter(logs, level, limit, start, end)

    def summarize(self, file_path: str) -> Dict[str, int]:
        """Parse and summarize log levels."""
        self.handle_invalid_file_path(file_path)
        logs = self.analyze(file_path)
        return self.summary.count_levels(logs)

    def print_table(self, data: List[dict]) -> None:
        """Print a user-friendly table to the terminal."""
        print(self.exporter.to_table(data))

    def export_csv(self, data: List[dict], path: str) -> None:
        """Export data to CSV file."""
        self.exporter.to_csv(data, path)

    def export_json(self, data: List[dict], path: str) -> None:
        """Export data to JSON file."""
        self.exporter.to_json(data, path)
