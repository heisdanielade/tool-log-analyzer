from datetime import datetime
from typing import Optional

DEFAULT_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S,%f"

def parse_date(date_str: str, fmt: str = "%Y-%m-%d %H:%M:%S,%f") -> Optional[datetime]:
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, fmt)
    except ValueError:
        # Try to fall back without milliseconds
        try:
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return None