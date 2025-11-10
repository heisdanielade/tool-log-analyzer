from typing import List
import csv
import json
from tabulate import tabulate

from .utils.string import truncate


class Exporter:
    def to_table(self, data: List[dict]) -> str:
        """Convert the list of dicts to a pretty table string."""
        if not data:
            return "No data to display."

        # build headers
        headers = []
        for item in data:
            for k in item.keys():
                if k not in headers:
                    headers.append(k)

        rows = [[truncate(item.get(h, "")) for h in headers] for item in data]
        return tabulate(rows, headers=headers, tablefmt="grid")  # type: ignore

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
