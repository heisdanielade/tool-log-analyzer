import sys
import pyfiglet
import typer
import click
from colorama import init, Fore
from core.config import ConfigManager
from core.analyzer import LogAnalyzer

init(autoreset=True)

app = typer.Typer(help="Log Analyzer CLI: Parse, filter, summarize logs.")
config_app = typer.Typer(help="Manage user configurations.")
app.add_typer(config_app, name="config")

analyzer = LogAnalyzer()

DEFAULT_FORMAT = "simple"


@app.command()
def interactive():
    """
    Start interactive Log Analyzer CLI session.
    """
    ascii_art = pyfiglet.figlet_format("Log Analyzer", font="slant")
    print(ascii_art)

    while True:
        try:
            command = input("log-analyzer>> ").strip()
            if command in ("exit", "quit", "q"):
                print("\nGoodbye!\n")
                break
            if command:
                sys.argv = ["main.py"] + command.split()
                try:
                    app(standalone_mode=False)
                except click.exceptions.ClickException as e:
                    print(Fore.RED + f"(e) {e.format_message()}\n")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!\n")
            break


@app.command()
def analyze(
    file: str = typer.Option(None, "--file", "-f", help="Path to log file"),
    parse_format: str = typer.Option(
        DEFAULT_FORMAT, "--format", "-p", help="Parsing format/profile")
):
    """Parse and display all log entries."""
    entries = analyzer.analyze(file)
    analyzer.print_table(entries)
    typer.echo(Fore.GREEN + f"Analyzed with {parse_format} format")


@app.command()
def summary(
        file: str = typer.Option(None, "--file", "-f",
                                 help="Path to log file"),
        parse_format: str = typer.Option(
            DEFAULT_FORMAT, "--format", "-p", help="Parsing format/profile"),
        output: str = typer.Option(
            None, "--output", "-o", help="CSV output file (optional)")
):
    """Generate summary of log levels."""
    counts = analyzer.summarize(file)
    summary_data = [{"level": k, "count": v} for k, v in counts.items()]
    analyzer.print_table(summary_data)

    typer.echo(Fore.GREEN +
               f"Summarized with {parse_format} format, output to {output}")


@app.command()
def filter(
    file: str = typer.Option(None, "--file", "-f", help="Path to log file"),
    parse_format: str = typer.Option(
        DEFAULT_FORMAT, "--format", "-p", help="Parsing format/profile"),
    level: str = typer.Option(
        None, "--level", "-l", help="Filter by log level"),
    limit: int = typer.Option(
        None, "--limit", "-lm", help="Result data limit (optional)"),
    start: str = typer.Option(
        None, "--start", "-s", help="Start date (YYYY-MM-DD)"),
    end: str = typer.Option(
        None, "--end", "-e", help="End date (YYYY-MM-DD)")
):
    """Filter logs by level and/or date range."""
    entries = analyzer.filter_logs(file, level, limit, start, end)
    analyzer.print_table(entries)

    typer.echo(Fore.GREEN +
               f"Filtered with level={level}, date_range={start} to {end}, result_limit={limit} format={parse_format}")


@app.command()
def export(
    file: str = typer.Option(None, help="Log file path (default from config)"),
    type: str = typer.Argument(..., help="To CSV or JSON file"),
    output: str = typer.Argument(..., help="Output CSV file"),
    level: str = typer.Option(None, help="Filter by log level"),
    limit: int = typer.Option(None, help="Result data limit, 00 for all data"),
    start: str = typer.Option(None, help="Start datetime"),
    end: str = typer.Option(None, help="End datetime")
):
    """Parse, filter and export logs to CSV or JSON."""
    entries = analyzer.filter_logs(file, level, limit, start, end)
    dot_index = output.rfind(".")
    file_extension = output[dot_index+1:].lower()
    export_type = type.lower()

    if export_type == "csv" and file_extension == "csv":
        analyzer.export_csv(entries, output)
    elif export_type == "json" and file_extension == "json":
        analyzer.export_json(entries, output)
    else:
        print(Fore.RED + "Invalid file type or combination")
        print(Fore.RED + f"{export_type=}, {file_extension=}")
        return

    typer.echo(f"Exported {len(entries)} entries to {output}\n")


@config_app.command("set")
def set_config(
    default_file: str = typer.Option(
        None, "--default-file", help="Default log file path"),
    parse_format: str = typer.Option(
        None, "--format", help="Default parsing format/profile")
):
    """Save user configurations."""
    cm = ConfigManager()
    if default_file:
        cm.set("default_file", default_file)
    if format:
        cm.set("format", parse_format)
    cm.save()
    typer.echo("Configuration updated.")


@config_app.command("show")
def show_config():
    """Display current configurations."""
    cm = ConfigManager()
    config = cm.all()
    if not config:
        typer.echo(Fore.YELLOW + "No config set yet.")
    else:
        typer.echo("Current Configuration:\n")
        for key, value in config.items():
            typer.echo(f"- {key}: {value}")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No subcommand given
        interactive()
    else:
        # Subcommands or flags given
        app()
