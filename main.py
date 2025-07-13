import pyfiglet
import typer

from core import config

app = typer.Typer(help="Log Analyzer CLI: Parse, filter, summarize logs.")
config_app = typer.Typer(help="Manage user configurations.")
app.add_typer(config_app, name="config")

ascii_art = pyfiglet.figlet_format("Log Analyzer", font="slant")
print(ascii_art)


default_parsing_format = "simple"


@app.command()
def analyze(
    file: str = typer.Option(..., "--file", "-f", help="Path to log file"),
    format: str = typer.Option(
        default_parsing_format, "--format", "-p", help="Parsing format/profile")
):
    """Parse and display all log entries."""
    # TODO: Load config if needed
    # TODO: Create LogAnalyzer, LogParser instances
    # TODO: Parse and print results as table
    typer.echo(f"Analyzing {file} with {format} format")
    pass


@app.command()
def summary(
        file: str = typer.Option(..., "--file", "-f", help="Path to log file"),
        format: str = typer.Option(
            default_parsing_format, "--format", "-p", help="Parsing format/profile"),
        output: str = typer.Option(
            None, "--output", "-o", help="CSV output file (optional)")
):
    """Generate summary of log levels."""
    # TODO: Load config if needed
    # TODO: Create LogAnalyzer, LogSummary
    # TODO: Print summary or export to CSV
    typer.echo(
        f"Summarizing {file} with {format} format, output to {output}")
    pass


@app.command()
def filter(
    file: str = typer.Option(..., "--file", "-f", help="Path to log file"),
    format: str = typer.Option(
        default_parsing_format, "--format", "-p", help="Parsing format/profile"),
    level: str = typer.Option(
        None, "--level", "-l", help="Filter by log level"),
    start: str = typer.Option(
        None, "--start", "-s", help="Start date (YYYY-MM-DD)"),
    end: str = typer.Option(
        None, "--end", "-e", help="End date (YYYY-MM-DD)"),
    limit: int = typer.Option(
        None, "--limit", "-lm", help="Result data limit (optional)"),
    output: str = typer.Option(
        None, "--output", "-o", help="CSV output file (optional)")
):
    """Filter logs by level and/or date range."""
    # TODO: Load config if needed
    # TODO: Create LogAnalyzer, LogSummary
    # TODO: Print or export filtered logs
    typer.echo(
        f"Filtering {file} with level={level}, date_range={start} to {end}, result_limit={limit} format={format}")
    pass


@config_app.command("set")
def set_config(
    default_file: str = typer.Option(
        None, "--default-file", help="Default log file path"),
    format: str = typer.Option(
        None, "--format", help="Default parsing format/profile")
):
    """Save user configurations."""
    config_manager = config.ConfigManager()
    if default_file:
        config_manager.set("default_file", default_file)
    if format:
        config_manager.set("format", format)
    config_manager.save()
    typer.echo("Configurations updated.")


@config_app.command("show")
def show_config():
    """Display current configurations."""
    config_manager = config.ConfigManager()
    cfg = config_manager.load()
    typer.echo(f"Current Configuration:\n{cfg}")


if __name__ == "__main__":
    app()
