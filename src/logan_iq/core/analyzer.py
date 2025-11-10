import os
from typing import List, Dict, Optional
from colorama import init, Fore

from .parser import LogParser
from .filter import LogFilter
from .summarizer import LogSummarizer
from .exporter import Exporter

init(autoreset=True)


class LogAnalyzer:
    """High-level API for CLI commands to analyze, filter, summarize, export logs."""

    def __init__(self, parse_format: str, custom_regex: Optional[str] = None):
        self.parse_format = parse_format
        self.parser = LogParser(parse_format, custom_regex=custom_regex)
        self.filter = LogFilter()
        self.summarize = LogSummarizer()
        self.exporter = Exporter()

    def _validate_file(self, file_path: str):
        if file_path and not os.path.exists(file_path):
            print(Fore.RED + f"No such file or directory: {file_path}")
            exit(1)

    def analyze(self, file_path: str) -> List[dict]:
        self._validate_file(file_path)
        return self.parser.parse_file(file_path)

    def filter_logs(
        self,
        file_path: str,
        level: Optional[str] = None,
        limit: Optional[int] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[dict]:
        logs = self.analyze(file_path)
        filtered = self.filter.filter(logs, level, limit, start, end)

        if search:
            filtered = self.filter.filter_by_keyword(logs=filtered, keyword=search, parse_fmt=self.parse_format)

        return filtered

    def summarize(self, file_path: str) -> Dict[str, int]:
        logs = self.analyze(file_path)
        return self.summarize.count_levels(logs)

    def summarize_by_day(
            self,
            file_path: str,
            day: str,
            day_fmt: str = "%Y-%m-%d",
            log_fmt: str = "%Y-%m-%d %H:%M:%S,%f",
    ) -> Dict[str, int]:
        """Return counts per log level for a specific day."""
        logs = self.analyze(file_path)
        return self.summarize.count_logs_in_a_day(logs, day, day_fmt=day_fmt, log_fmt=log_fmt)

    def print_table(self, data: List[dict]):
        print(self.exporter.to_table(data))

    def export_csv(self, data: List[dict], path: str):
        self.exporter.to_csv(data, path)

    def export_json(self, data: List[dict], path: str):
        self.exporter.to_json(data, path)
