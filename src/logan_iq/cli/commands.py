import os
from datetime import datetime

import typer
from colorama import init, Fore, Style

from .interactive import interactive_mode
from ..core.config import ConfigManager
from ..core.analyzer import LogAnalyzer

init(autoreset=True)

app = typer.Typer(help="Logan-IQ: Analyze, parse, filter & summarize logs.")
app.command(name="interactive")(lambda: interactive_mode(app))
config_app = typer.Typer(help="Manage user configurations.")
app.add_typer(config_app, name="config")

cm = ConfigManager()


# ---------------------------
# Helper
# ---------------------------
def resolve_file_and_format(file: str, parse_format: str):
    file = file or cm.get("default_file")
    parse_format = parse_format or cm.get("format", "simple")

    if not file:
        typer.echo(Fore.RED + "No log file specified. Set a default via 'config set' or pass --file.")
        raise typer.Exit()
    return file, parse_format


# ---------------------------
# CLI Commands
# ---------------------------
@app.command()
def analyze(
        file: str = typer.Option(None, "--file", "-f", help="Path to log file"),
        parse_format: str = typer.Option(None, "--format", "-p", help="Parsing format/profile"),
        regex: str = typer.Option(None, "--regex", "-r", help="Custom regex (use with --format custom)")
):
    """Parse and display all log entries."""
    file, parse_format = resolve_file_and_format(file, parse_format)
    analyzer = LogAnalyzer(parse_format, regex)
    entries = analyzer.analyze(file)
    analyzer.print_table(entries)
    typer.echo("\n" + Fore.GREEN + f"Analyzed '{file}' with {parse_format} format\n")


@app.command()
def summarize(
        file: str = typer.Option(None, "--file", "-f", help="Path to log file"),
        parse_format: str = typer.Option(None, "--format", "-p", help="Parsing format/profile"),
        regex: str = typer.Option(None, "--regex", "-r", help="Custom regex (use with --format custom)"),
        day: str = typer.Option(None, "--day", "-d", help="Summarize number of log entries for a specific day YYYY-MM-DD")
):
    """Generate a summary of log levels. (Optional) Can be summarized by a specific day."""
    file, parse_format = resolve_file_and_format(file, parse_format)
    analyzer = LogAnalyzer(parse_format=parse_format, custom_regex=regex)

    if day:
        counts = analyzer.summarize_by_day(file, day)
    else:
        counts = analyzer.summarize(file)

    summary_data = [{"level": k, "count": v} for k, v in counts.items()]
    analyzer.print_table(summary_data)
    typer.echo("\n" + Fore.GREEN + f"Summarized '{file}' with format={parse_format}, day={day}\n")


@app.command()
def filter_logs(
        file: str = typer.Option(None, "--file", "-f", help="Path to log file"),
        parse_format: str = typer.Option(None, "--format", "-p", help="Parsing format/profile"),
        regex: str = typer.Option(None, "--regex", "-r", help="Custom regex (use with --format custom)"),
        level: str = typer.Option(None, "--level", "-l", help="Log level i.e., INFO, ERROR, WARNING"),
        limit: int = typer.Option(None, "--limit", "-lm", help="Result set limit (optional)"),
        start: str = typer.Option(None, "--start", "-st", help="Start date (log timestamp)"),
        end: str = typer.Option(None, "--end", "-e", help="End date (log timestamp"),
        keyword_search: str = typer.Option(None, "--search", "-s", help="Filter logs by keyword in the message field.")
):
    """Filter logs by level and/or date range."""
    file, parse_format = resolve_file_and_format(file, parse_format)
    analyzer = LogAnalyzer(parse_format, regex)
    entries = analyzer.filter_logs(file, level, limit, start, end, keyword_search)
    analyzer.print_table(entries)
    typer.echo("\n" + Fore.GREEN + f"Filtered '{file}' with format={parse_format}, level={level}, date_range={start} to {end}, limit={limit}\n")


@app.command()
def export_logs(
        file_type: str = typer.Argument(...),
        file: str = typer.Option(None, "--file", "-f", help="Path to log file"),
        parse_format: str = typer.Option(None, "--format", "-p", help="Parsing format/profile"),
        regex: str = typer.Option(None, "--regex", "-r", help="Custom regex (use with --format custom)"),
        output: str = typer.Option(None, "--output", "-o", help="CSV/JSON output file (optional)"),
        level: str = typer.Option(None, "--level", "-l", help="Log level i.e., INFO, ERROR, WARNING"),
        limit: int = typer.Option(None, "--limit", "-lm", help="Result set limit (optional)"),
        start: str = typer.Option(None, "--start", "-st", help="Start date (log timestamp)"),
        end: str = typer.Option(None, "--end", "-e", help="End date (log timestamp"),
        keyword_search: str = typer.Option(None, "--search", "-s", help="Filter logs by keyword in the message field.")
):
    """Parse, filter and export logs to CSV or JSON."""
    file, parse_format = resolve_file_and_format(file, parse_format)
    analyzer = LogAnalyzer(parse_format, regex)
    entries = analyzer.filter_logs(file, level, limit, start, end, keyword_search)

    export_type = file_type.lower()
    if output is None:
        base_name = os.path.splitext(os.path.basename(file))[0]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output = f"logan-iq-logs/{base_name}_by_logan-iq_{timestamp}.{export_type}"

    # dot_index = output.rfind(".")
    # file_extension = output[dot_index + 1:].lower()

    if export_type == "csv":
        analyzer.export_csv(entries, output)
    elif export_type == "json":
        analyzer.export_json(entries, output)
    else:
        # print(Fore.RED + "Invalid file type or combination")
        # print(Fore.RED + f"{export_type=}, {file_extension=}")
        typer.echo(Fore.RED + f"Unsupported export type: {type}")
        raise typer.Exit()


    typer.echo("\n" + Fore.GREEN + f"Exported {len(entries)} entries to [{output}]\n")


# ---------------------------
# Config Commands
# ---------------------------
@config_app.command("set")
def set_config(
        default_file: str = typer.Option(None, "--default-file", "-df"),
        parse_format: str = typer.Option(None, "--format"),
        custom_regex: str = typer.Option(None, "--custom-regex", "-cr")
):
    """Save user configurations."""
    if default_file:
        cm.set("default_file", default_file)
    if parse_format:
        cm.set("format", parse_format)
    if custom_regex:
        cm.set("custom_regex", custom_regex)
    cm.save()
    typer.echo("\n"+ Fore.GREEN + "Configuration updated.")

@config_app.command("show")
def show_config():
    """Display current configurations."""
    config = cm.all()
    if not config:
        typer.echo("\n" + Fore.YELLOW + "No configuration set yet.\n")
    else:
        typer.echo("Current Configurations:\n")
        for key, value in config.items():
            typer.echo(f"- {key}:" + Fore.CYAN + f" {value}" + Style.RESET_ALL)
        typer.echo("")

@config_app.command("delete")
def delete_config(
        key: str = typer.Option(None, "--key", "-k"),
        delete_all: bool = typer.Option(False, "--all")
):
    """Delete a config key or clear all."""
    if delete_all:
        confirm = typer.confirm(Fore.YELLOW + "Are you sure you want to delete ALL configuration data? This cannot be undone.")
        if not confirm:
            typer.echo("\n" + Fore.CYAN + "Operation cancelled.\n")
            raise typer.Exit()
        cm.delete()
        typer.echo("\n" + Fore.GREEN + "All configuration deleted.\n")
        return

    if key:
        if cm.get(key) is None:
            typer.echo("\n" + Fore.YELLOW + f"No configuration found for key: {key}\n")
            raise typer.Exit()
        cm.delete(key)
        typer.echo("\n" + Fore.GREEN + f"Deleted configuration key: {key}\n")
        return

    typer.echo("\n" + Fore.YELLOW + "Specify --key <name> to delete a specific config or --all to delete all configurations.")

