import os
import sys


def supports_hyperlinks() -> bool:
    """
    Detect if the terminal supports ANSI hyperlinks.
    Works in most modern terminals (VS Code, iTerm2, Windows Terminal).
    """
    if os.getenv("FORCE_HYPERLINK"):
        return True
    if not sys.stdout.isatty():
        return False
    term = os.getenv("TERM", "")
    colorterm = os.getenv("COLORTERM", "")
    term_program = os.getenv("TERM_PROGRAM", "")
    return any(
        [
            "xterm-kitty" in term,
            "vscode" in term_program.lower(),
            "iTerm.app" in term_program,
            "WezTerm" in term_program,
            "WindowsTerminal" in term_program,
            "truecolor" in colorterm,
        ]
    )


def hyperlink(text: str, url: str) -> str:
    """
    Return a clickable hyperlink if supported, otherwise fallback text.
    """
    if supports_hyperlinks():
        return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"
    else:
        return f"{text} ({url})"
