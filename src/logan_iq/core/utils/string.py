def truncate(s: str, width: int = 70) -> str:
    """Truncate string to fit width, append ellipsis if necessary."""
    s = str(s)
    return s if len(s) <= width else s[: width - 3] + "..."
