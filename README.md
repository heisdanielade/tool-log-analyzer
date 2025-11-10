# Logan-iq: Multi-Log Analysis Tool

<p align="center">
  <img src="https://img.shields.io/pypi/v/logan-iq?color=blue&label=PyPI%20version" alt="PyPI version">
  <img src="https://img.shields.io/github/actions/workflow/status/heisdanielade/tool-log-analyzer/.github/workflows/test.yml?label=build&logo=github" alt="Build Status">
  <img src="https://img.shields.io/pypi/pyversions/logan-iq?logo=python&label=python%20versions" alt="Python versions">
  <img src="https://img.shields.io/pypi/dm/logan-iq" alt="Downloads">
  <img src="https://img.shields.io/github/issues/heisdanielade/tool-log-analyzer" alt="Last Commit">

[//]: # (  <img src="https://img.shields.io/github/last-commit/heisdanielade/tool-log-analyzer?logo=github&label=Last%20Commit" alt="Last Commit">)
</p>

An interactive command-line tool for parsing, filtering, summarizing, and exporting log files.
Supports multiple log formats with flexible regex patterns and fully customizable user preferences.

#### ⚠️ Installation Notice

Version **1.0.1** contains unintended scripts and **should not be used**.  
Please install **v1.0.2 or later** for proper functionality and stability.

## Features

- Parse logs using default or custom regex patterns
- Interactive and user-friendly CLI interface
- Filter logs by level, date range, keyword or result limit
- Generate summary tables with counts per level or per day
- Export logs in CSV or JSON formats
- Clean, colorful, and easy-to-read terminal output

## Install

Package is available on [PyPI](https://pypi.org/project/logan-iq/)

```bash
  pip install logan-iq
  
  logan-iq interactive
```

This makes the `logan-iq` command available in your terminal and then runs the **interactive mode**.

#### 🖥️ Startup

![Logan-iq Startup Screenshot](https://raw.githubusercontent.com/heisdanielade/tool-log-analyzer/refs/heads/main/assets/screenshots/startup.png)

## How it Works

Core flow:

1. **Load Config or Defaults:**

Loads user preferences from config.json if it exists. CLI arguments always override the config file. If no file is provided and no config exists, the app prompts the user to specify a file.

2. **Parse Log File:**

Each log line is converted into a structured dictionary with fields like `datetime`, `level`, `message`,and optionally `ip` or other fields depending on the format.

3. **Filter (Optional):**

Narrow results by log level, date range, keyword(s) search or limit the number of entries displayed.
<br>**NOTE:** Keyword search covers `message`, `method`, `path` and `status`/`status_code` if they exist in json logs.

4. **Analyze or Summarize:**

Display logs in a terminal table or generate summary reports.

5. **Export (Optional):**

Export filtered data to CSV or JSON for further analysis.

## Available Formats

You can supply your own regex directly via CLI or in saved configs `custom_regex`.
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

- **json** → JSON formatted logs (one object per line)

```json
{
  "datetime": "2025-08-28 12:34:56",
  "level": "INFO",
  "message": "Server started",
  "method": "GET",
  "status": 200,
  "path": "/api/v1/users"
}
```

- **custom** → Any user-defined regex
  Example (inline via CLI):

```bash
  logan-iq analyze --file logs/app.log --format custom --regex "^(?P<ts>\S+) (?P<level>\w+) (?P<msg>.*)$"
```

Or define in saved configs:

```json
{
  "default_file": "logs/custom_app.log",
  "format": "custom",
  "custom_regex": "^(?P<ts>\\S+) (?P<level>\\w+) (?P<msg>.*)$"
}
```

## Running the CLI

Once installed, commands can be run directly via `logan-iq`:

- Help
```bash
  logan-iq --help # General help 
  
  # Command specific help
  logan-iq analyze --help
  logan-iq summarize --help
  logan-iq filter-logs --help
  logan-iq export-logs --help
  logan-iq config --help
  logan-iq config set --help
  logan-iq config show --help
  logan-iq config delete --help
```

- Interactive Mode

```bash
    logan-iq interactive
    
    logan-iq>> analyze --file app.log
    logan-iq>> summarize --file app.log --format simple
    
    logan-iq>> filter-logs --search "500 Server Error"
    logan-iq>> filter-logs --level ERROR --start 2025-11-01 --end 2025-11-08
    logan-iq>> export-logs csv --file app.log --output exported_logs/output.csv
    logan-iq>> export-logs json --file app.log --output exported_logs/output.json
    logan-iq>> export-logs json --search "'404 Client Error" --file app.log --output exported_logs/output.json
    
    logan-iq>> config set --default-file app.log --format simple
    logan-iq>> config show
    logan-iq>> config delete --key default_file
    
    logan-iq>> exit

```

- Analyze Logs

```bash
  logan-iq analyze --file/ path/to/logfile.log --format apache
```

- Custom Regex

```bash
  logan-iq analyze --file app.log --format custom --regex "^(?P<ts>\\S+) (?P<msg>.*)$"
```

- Summarize Log Levels

```bash
  logan-iq summarize --file path/to/logfile.log
```

- Filter Log Levels

```bash
  logan-iq filter-logs --file app.log --level ERROR --search "500 Server Error" --start 2025-11-01 --end 2025-11-08
```

- Export Logs

```bash
  logan-iq export-logs --file path/to/logfile.log --output csv
```

- Shorthand flags

You can also use shorthand flags like:
```bash
  -f     # --file 
  -df    # --default-file
  -r     # --custom-regex
  -cr    # --custom-regex (for configs)
  -l     # --level
  -s     # --search
  -lm    # --limit
  -st    # --start
  -e     # --end
  -d     # --day
  -o     # --output
  -k     # --key
```

## Configuration

On installation, a `.logan-iq_config.json` is created on the user's system in the root directory.

- To show configurations

```bash
    logan-iq interactive
    logan-iq>> config show
```

- To modify configurations

```bash
    logan-iq>> config set --default-file logs/access.log --format nginx
    logan-iq>> config set --format custom --custom-regex "^(?P<ts>\\S+) (?P<msg>.*)$"
```

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
  "custom_regex": "^(?P<ts>\\S+) (?P<msg>.*)$"
}
```

- CLI args always override config values.

- If neither CLI args nor config exist, **the app prompts for a file**.

### Deleting configuration entries

You can delete configuration entries using the `config delete` command.

- Delete a single key:

```bash
    logan-iq config delete default_file
```

- Delete all keys (requires confirmation):

```bash
    logan-iq config delete all
```

If you run the command without either `--key` or `--all` you'll receive a helpful message explaining the available options.

## Dependencies

- CLI built with `Typer`
- Pretty tables via `Tabulate`
- Colored output via `PyFiglet`
- Unit testing via `Pytest`

---

## Contributing

Contributions are welcome! <br>
**NOTE:** Codebase docs i.e., docstrings, comments, files... must be in **_ENGLISH_**)

1. **Fork** the repo and clone it locally.  
2. **Create a virtual environment** and install dependencies: `pip install -e .`.  
3. **Run tests**: `pytest`.  
4. Create a **branch** from `main`: `git checkout -b feat/name` or `git checkout -b fix/name`.  
5. Make changes, **write tests**, and follow **PEP8**.  
6. Commit with **clear messages** and push your branch.  
7. Open a **Pull Request** for review.  
8. Report bugs via **Issues** with clear steps and logs.  
9. By contributing, you agree to the repo’s **license** and **Code of Conduct**.  
10. Be creative!

---