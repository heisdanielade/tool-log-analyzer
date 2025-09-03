# Log Analyzer CLI

![Version](https://img.shields.io/badge/version-1.0.1-blue) ![Issues](https://img.shields.io/github/issues/heisdanielade/tool-log-analyzer)

A Python command-line tool for parsing, filtering, summarizing, and exporting log files. Designed to handle multiple log formats with regex support and user-configurable preferences.

## Features

- Parse logs using regex patterns (default or custom)
- Filter logs by level, date range, or limit
- Generate summary tables (count by log level)
- Export logs to CSV or JSON
- Interactive CLI with `typer`
- Colorful output and clean formatting
- Easily testable and extensible

## How it Works

Core flow:

1. **Load Config or Use Defaults**
   App loads user preferences and regex pattern. Falls back to a default if none is provided.
2. Parse Log File
   Each line in the log is converted into a dictionary with structured fields (like `datetime`, `level`, `message`, `ip`, etc.).
3. **Filter (Optional)**
   Narrow results by level, date, or limit.
4. **Analyze or Summarize**
   Display logs in a table or generate summary counts.
5. **Export (Optional)**
   Export results to CSV/JSON for further analysis.

## Available Formats

This tool comes with a few pre-configured log formats out of the box.
You can also supply your own regex directly via CLI or in `config.json`.

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

- **custom (user-defined regex)** → Any custom format
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
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the App

In interactive mode, commands are written without **_python main.py_**

- Interactive Mode

```bash
python main.py
log-analyzer>> analyze --file logs/access.log --format nginx
```

- Analyze All Logs

```bash
python main.py analyze --file path/to/logfile.log --format apache
```

- Analyze with Custom Regex

```bash
python main.py analyze --file app.log --format custom --regex "^(?P<ts>\S+) (?P<msg>.*)$"
```

- Summary of Log Levels

```bash
python main.py summary --file path/to/logfile.log
```

- Export Logs to File

```bash
python main.py export --file path/to/logfile.log --output-format csv --output-path logs.csv
```

## Configuration

You can define defaults in `config.json` at the project root.

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

## Testing

Run tests from root directory:

```bash
pytest -s
```

Covers:

- Log parsing (valid and invalid formats, files)
- Log filtering (by level, date and limit)
- Summary generation
- Error handling

## Project Structure

```
.
├── tool-log-analyzer/             # Core logic
├───core/
│       ├── parser.py
│       ├── filter.py
│       ├── summary.py
│       ├── exporter.py
│       └── config.py
├── tests/                # Unit tests
├── main.py               # CLI entry point
├── requirements.txt
└── config.json  # Optional config file
```

## Additional Info

This project was inspired by real-world needs for log analysis tools and designed with flexibility in mind.
It incorporates design patterns such as separation of concerns, configuration loading, and extensibility through modular classes.

- `Typer` for CLI
- `PyFiglet` for colored output
- `Tabulate` for pretty tables
- `Pytest` for testing

---

Developed by **[heisdanielade](https://github.com/heisdanielade)**

---
