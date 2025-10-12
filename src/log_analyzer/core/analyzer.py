import os
from typing import List, Dict, Optional

from colorama import init, Fore

from .config import ConfigManager
from .parser import LogParser
from .filter import LogFilter
from .summarizer import LogSummarizer
from .exporter import Exporter


init(autoreset=True)


class LogAnalyzer:
    """Analyzer class to associate CLI command with designated feature."""

    def __init__(self, config_file: str = "src/config.json"):
        self.config_manager = ConfigManager(config_file)
        self.config = self.config_manager.load()

        format_name = self.config.get("format", "simple")
        custom_regex = self.config.get("custom_regex")
        self.parser = LogParser(format_name, custom_regex=custom_regex)
        self.filter = LogFilter()
        self.summary = LogSummarizer()
        self.exporter = Exporter()

    def handle_invalid_file_path(self, file) -> None:
        """
        Helper method to handle FileNotFoundError if user provided
        file path does not exists.
        """
        if file and not os.path.exists(file):
            print(Fore.RED + f"No such file or directory: {file}")
            exit(1)

    def analyze(self, file_path: Optional[str] = None) -> List[dict]:
        """Parse entire log file."""
        if not file_path:
            file_path = self.config.get("default_file")
        self.handle_invalid_file_path(file_path)
        return self.parser.parse_file(file_path)  # type: ignore

    def filter_logs(
        self,
        file_path: Optional[str] = None,
        level: Optional[str] = None,
        limit: Optional[int] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
    ) -> List[dict]:
        """Parse and filter logs."""
        self.handle_invalid_file_path(file_path)
        logs = self.analyze(file_path)
        return self.filter.filter(logs, level, limit, start, end)

    def summarize(self, file_path: Optional[str] = None) -> Dict[str, int]:
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
