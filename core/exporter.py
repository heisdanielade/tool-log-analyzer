from typing import List
import csv
from tabulate import tabulate


class Exporter:
    def to_table(self, data: List[dict]) -> str:
        """Convert list of dicts to a pretty table string."""
        if not data:
            return "No data to display."

        headers = data[0].keys()
        rows = [item.values() for item in data]
        table = tabulate(rows, headers=headers,  # type: ignore
                         tablefmt="grid")
        return table

    def to_csv(self, data: List[dict], path: str) -> None:
        """Write list of dicts to CSV file."""
        if not data:
            print("No data to export.")
            return

        headers = data[0].keys()
        with open(path, "w", newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)

    # TODO: Add JSON export
    # TODO: Add Excel (xlsx) export
