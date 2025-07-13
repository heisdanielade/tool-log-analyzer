import pyfiglet
import typer

app = typer.Typer()

ascii_art = pyfiglet.figlet_format("Log Analyzer", font="slant")
print(ascii_art)


default_parsing_format = "simple"


@app.command()
def analyze(file: str, format: str = default_parsing_format):
    # Call LogAnalyzer with LogParser
    pass


@app.command()
def summary(file: str, format: str = default_parsing_format, output: str = None):
    # Summarize log levels
    pass


@app.command()
def filter(
    file: str,
    format: str = default_parsing_format,
    level: str = None,
    start: str = None,
    end: str = None,
    limit: int = None,
    output: str = None
):
    # Filter logs
    pass


config_app = typer.Typer()
app.add_typer(config_app, name="config")


@config_app.command("set")
def set_config(default_file: str = None, format: str = None):  # type: ignore
    # Save preferences
    pass


@config_app.command("show")
def show_config():
    # Print current config
    pass


if __name__ == "__main__":
    app()
