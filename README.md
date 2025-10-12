# Log Analyzer CLI

![Version](https://img.shields.io/badge/version-1.0.1-blue) ![Issues](https://img.shields.io/github/issues/heisdanielade/tool-log-analyzer)

A Python command-line tool for parsing, filtering, summarizing, and exporting log files. Designed to handle multiple log formats with regex support and user-configurable preferences.

## Features

- Parse logs using regex patterns (default or custom)
- Filter logs by level, date range, or limit
- Generate summary tables
- Export logs to CSV or JSON
- Interactive CLI with `typer`
- Colorful output and clean formatting
- Easily testable and extensible

## How it Works

Core flow:

1. **Load Config or Defaults:**
   Loads user preferences from config.json if it exists. CLI arguments always override the config file. If no file is provided and no config exists, the app prompts the user to specify a file.
2. **Parse Log File:**

Each log line is converted into a structured dictionary with fields like `datetime`, `level`, `message`,and optionally `ip` or other fields depending on the format.

3. **Filter (Optional):**

Narrow results by log level, date range, or limit the number of entries displayed.

4. **Analyze or Summarize:**

Display logs in a terminal table or generate summary reports.

5. **Export (Optional):**

Export filtered data to CSV or JSON for further analysis.

## Available Formats

You can supply your own regex directly via CLI or in `config.json`.
Or use the Built-in formats:

- **simple** → generic logs with `datetime`, `level` and `message`

```yaml
2025-08-28 12:34:56 [INFO] Server started: Listening on port 8080
```

- **apache** → Apache access logs (common format)

```yaml
192.200.2.2 - - [28/Aug/2025:12:34:56 +0000] "GET /index.html HTTP/1.1" 200 512
```

- **nginx** → Nginx access logs (combined format, includes referrer & user-agent)

```yaml
192.100.1.1 - - [28/Aug/2025:12:34:56 +0000] "GET /index.html HTTP/1.1" 200 1024 "http://example.com" "Mozilla/5.0"
```

- **custom** → Any user-defined regex
  Example (inline via CLI):

```bash
python main.py analyze --file logs/app.log --format custom --regex "^(?P<ts>\S+) (?P<level>\w+) (?P<msg>.*)$"

```

Or define in `config.json`:

```json
{
  "default_file": "logs/custom_app.log",
  "format": "custom",
  "custom_regex": "^(?P<ts>\\S+) (?P<level>\\w+) (?P<msg>.*)$"
}
```

## Setup Instructions

1. Clone the repository

```bash
  git clone https://github.com/heisdanielade/tool-log-analyzer.git
  cd tool-log-analyzer
```

2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows
venv\Scripts\activate
```

3. Install dependencies in editable mode

```bash
pip install -e .
```

This makes the log-analyzer CLI available globally in your environment, and any code changes in `src/log_analyzer` are immediately reflected without reinstalling.

## Running the CLI

Once installed, commands can be run directly via `log-analyzer`:

- For Interactive Mode

```bash
log-analyzer interactive
log-analyzer>> analyze --file logs/access.log --format nginx
```

- Analyze Logs

```bash
log-analyzer analyze --file path/to/logfile.log --format apache
```

- Custom Regex

```bash
log-analyzer analyze --file app.log --format custom --regex "^(?P<ts>\S+) (?P<msg>.*)$"
```

- Summarize Log Levels

```bash
log-analyzer summarize --file path/to/logfile.log
```

- Export Logs

```bash
log-analyzer export --file path/to/logfile.log --output-format csv --output-path logs.csv
```

## Configuration

Defaults can be set in `src/config.json`:

Example with built-in format:

```json
{
  "default_file": "logs/server_logs.log",
  "format": "nginx"
}
```

Example with custom format:

```json
{
  "default_file": "logs/app.log",
  "format": "custom",
  "custom_regex": "^(?P<ts>\\S+) (?P<level>\\w+) (?P<msg>.*)$"
}
```

- CLI args always override config values.

- If neither CLI args nor config exist, **the app prompts for a file**.

## Testing

Run tests from root directory:

```bash
pytest -s
```

- Validates parsing, filtering, summarization, export, and error handling.
- Editable install ensures tests can import modules with absolute imports.

## Project Structure

```
.
├── src/log_analyzer/          # Core logic
│   ├── __init__.py
│   ├── __main__.py            # CLI entry point
│   ├── core/
│   │    ├── analyzer.py
│   │    ├── parser.py
│   │    ├── filter.py
│   │    ├── summary.py
│   │    ├── exporter.py
│   │    └── config.py
│   │    └── helpers.py
│   └── tests/                 # Unit tests
├── LICENSE
├── README.md
├── pyproject.toml
└── venv/                      # Virtual environment (optional)

```

## Additional Info

- CLI built with `Typer`
- Pretty tables via `Tabulate`
- Colored output via `PyFiglet`
- Unit testing via `Pytest`

---

Developed by **[heisdanielade](https://github.com/heisdanielade)**

---
