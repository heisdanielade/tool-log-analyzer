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

1. Load Config or Use Defaults
   App loads user preferences and regex pattern. Falls back to a default if none is provided.
2. Parse Log File
   Each line in the log is converted into a dictionary with keys like `datetime`, `level`, and `message`.
3. Filter (Optional)
   You can narrow results by level, date, or number of results.
4. Analyze or Summarize
   The app can display all logs in a table or show a summary report of how many logs per level.
5. Export (Optional)
   You can export results to a file for further analysis.

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
log-analyzer>> analyze
```

- Analyze All Logs

```bash
python main.py analyze --file path/to/logfile.log
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

You can define your default log file name and parsing format type in a config file named `config.json` in the root directory.

```json
{
  "default_file": "logs/server_logs.log",
  "format": "simple"
}
```

## Testing

Run tests from root directory using:

```bash
pytest -s
```

The tests cover:

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

Developed by **[heisdanielade](https://www.heisdanielade.xyz/)**

---
