from typing import List
import csv
import json

from colorama import Fore, Style
from tabulate import tabulate

from .utils.string import truncate


class Exporter:
    def to_table(self, data: list[dict]) -> str:
        """Convert the list of dicts to a pretty table string with colorized levels."""
        if not data:
            return "No data to display."

        # Collect headers dynamically
        headers = []
        for item in data:
            for k in item.keys():
                if k not in headers:
                    headers.append(k)

        def colorize(level: str, text: str) -> str:
            """Return color-coded text for log levels."""
            level = str(level).upper()
            if level == "ERROR":
                return Fore.RED + text + Style.RESET_ALL
            elif level == "WARNING" or level == "WARN":
                return Fore.YELLOW + text + Style.RESET_ALL
            elif level == "DEBUG":
                return Fore.CYAN + text + Style.RESET_ALL
            elif level == "INFO":
                return Fore.GREEN + text + Style.RESET_ALL
            else:
                return text

        # Build table rows
        rows = []
        for item in data:
            row = []
            for h in headers:
                val = truncate(str(item.get(h, "")))
                if h.lower() == "level":
                    val = colorize(val, val)
                row.append(val)
            rows.append(row)

        return tabulate(rows, headers=headers, tablefmt="grid")

    def to_csv(self, data: List[dict], path: str) -> None:
        """Write a list of dicts to a CSV file."""
        if not data:
            print("No data to export.")
            return

        headers = data[0].keys()
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

    def to_json(self, data: List[dict], file_path: str) -> None:
        """Write JSON data to a file."""
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
