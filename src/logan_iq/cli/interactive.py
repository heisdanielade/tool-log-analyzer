import pyfiglet
import typer
from colorama import Fore, Style

from ..__version__ import __version__
from ..core.utils.terminal import hyperlink


# ---------------------------
# Interactive Mode
# ---------------------------
def interactive_mode(app: typer.Typer):

    ascii_art = pyfiglet.figlet_format("Logan-IQ", font="slant")
    print(Fore.CYAN + ascii_art + f"v{__version__}")
    print(Fore.CYAN + "By " + hyperlink("heisdanielade", "https://github.com/heisdanielade"))
    print(Fore.CYAN + "Type '--help' to see commands or 'exit' to quit.\n")

    while True:
        try:
            command = input(f"{Fore.BLUE}\033[1mlogan-iq>> \033[0m{Style.RESET_ALL}").strip()
            if command in ("exit", "quit", "q", "cancel", "interactive"):
                print("\nGoodbye..\n")
                break

            if command:
                import shlex
                import sys

                sys.argv = ["logan-iq"] + shlex.split(command)
                try:
                    app(standalone_mode=False)
                except typer.Exit:
                    pass
                except Exception as e:
                    print(Fore.RED + f"(e) {e}\n")

        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye..\n")
            break