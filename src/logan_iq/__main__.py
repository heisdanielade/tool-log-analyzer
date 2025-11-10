import sys

from .cli.commands import app
from .cli.interactive import interactive_mode


if __name__ == "__main__":
    if len(sys.argv) == 1:
        interactive_mode(app)
    else:
        app()
