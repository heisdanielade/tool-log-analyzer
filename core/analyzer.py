from core.config import ConfigManager
from core.parser import LogParser
from core.filter import LogFilter
from core.summary import LogSummary
from core.exporter import Exporter
from typing import List, Dict, Optional


class LogAnalyzer:
    def __init__(self, config_file: str = "config.json"):
        self.config_manager = ConfigManager(config_file)
        self.config = self.config_manager.load()

        format_name = self.config.get("format", "simple")
        self.parser = LogParser(format_name)
        self.filter = LogFilter()
        self.summary = LogSummary()
        self.exporter = Exporter()

    def analyze(self, file_path: Optional[str] = None) -> List[dict]:
        """Parse entire log file."""
        if not file_path:
            file_path = self.config.get("default_file")
        return self.parser.parse_file(file_path)  # type: ignore

    def filter_logs(
        self,
        file_path: Optional[str] = None,
        level: Optional[str] = None,
        limit: Optional[int] = None,
        start: Optional[str] = None,
        end: Optional[str] = None
    ) -> List[dict]:
        """Parse and filter logs."""
        logs = self.analyze(file_path)
        return self.filter.filter(logs, level, limit, start, end)

    def summarize(self, file_path: Optional[str] = None) -> Dict[str, int]:
        """Parse and summarize log levels."""
        logs = self.analyze(file_path)
        return self.summary.count_levels(logs)

    def print_table(self, data: List[dict]) -> None:
        """Print a user-friendly table to the terminal."""
        print(self.exporter.to_table(data))

    def export_csv(self, data: List[dict], path: str) -> None:
        """Export data to CSV file."""
        self.exporter.to_csv(data, path)
