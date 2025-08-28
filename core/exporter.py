from typing import List
import csv
import json
from tabulate import tabulate


class Exporter:
    def to_table(self, data: List[dict]) -> str:
        """Convert list of dicts to a pretty table string."""
        if not data:
            return "No data to display."

        def truncate(s, width=60):
            s = str(s)
            return s if len(s) <= width else s[: width - 3] + "..."

        headers = data[0].keys()
        rows = [[truncate(item[h]) for h in headers] for item in data]
        table = tabulate(rows, headers=headers, tablefmt="grid")  # type: ignore
        return table

    def to_csv(self, data: List[dict], path: str) -> None:
        """Write list of dicts to CSV file."""
        if not data:
            print("No data to export.")
            return

        headers = data[0].keys()
        with open(path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

    def to_json(self, data: list[dict], file_path: str) -> None:
        """Write JSON data to file."""
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
