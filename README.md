# PineScript Syntax Checker MCP Server

A Model Context Protocol (MCP) server and CLI script for checking PineScript syntax using TradingView's API. Forked from https://github.com/erevus-cn/pinescript_syntax_checker (thanks to erevus for the original work).

## Features

- Check PineScript syntax using TradingView's official API
- MCP-compatible server with httpx for async HTTP requests
- Fast CLI tool that can be run directly or via command
- CLI output drops the unused `scopes` array by default to save context/tokens (`--full-response` keeps it)
- Detailed error reporting with line and column information
- Modern Python tooling with `uv`, `ruff`, and `ty`
- Pre-commit hooks for code quality

## Requirements

- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended) or pip

## Quick Start

### Installation with uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/erevus-cn/pinescript_syntax_checker.git
cd pinescript_syntax_checker

# Sync dependencies (creates virtual environment automatically)
uv sync

# Run with uvx (no installation needed)
uvx pinescript-syntax-checker
```

### Installation with pip

```bash
# Install from source
pip install .

# Or install in editable mode for development
pip install -e .
```

## Usage

### Run as CLI script

The CLI is the simplest and fastest way to check PineScript syntax. It can be invoked in multiple ways:

```bash
# Method 1: Run directly (file is executable)
./pinescript_syntax_checker/pinescript_checker.py my_script.pine --pretty

# Method 2: Run via installed command
pinescript-checker my_script.pine --pretty

# Method 3: Run as module
python -m pinescript_syntax_checker.pinescript_checker my_script.pine --pretty

# Method 4: Run with uvx (no installation)
uvx --from . pinescript-checker my_script.pine --pretty
```

#### CLI Options

```bash
pinescript-checker --help

options:
  -h, --help            show this help message and exit
  --username USERNAME   TradingView username used for the request (default: admin)
  --pretty              Pretty-print JSON output
  --full-response       Return the raw TradingView payload (including rarely used 'scopes')
```

### Run as MCP server

Build and install the package, then run:

```bash
# Install the package
uv sync
uv pip install .

# Run the MCP server
pinescript-syntax-checker

# Or run directly with uvx
uvx --from . pinescript-syntax-checker
```

#### Add to Claude Desktop or Cline

Add this to your MCP configuration file:

```json
{
  "mcpServers": {
    "pinescript-syntax-checker": {
      "command": "uvx",
      "args": ["pinescript-syntax-checker"]
    }
  }
}
```

Or use the installed version:

```json
{
  "mcpServers": {
    "pinescript-syntax-checker": {
      "command": "pinescript-syntax-checker"
    }
  }
}
```

## Development

### Setup Development Environment

```bash
# Sync dependencies including dev tools
uv sync

# Install pre-commit hooks
uv run pre-commit install

# Run linting and formatting
uv run ruff check --fix
uv run ruff format

# Run type checking
uv run ty
```

### Development Tools

This project uses modern Python tooling:

- **uv**: Fast Python package manager and project manager
- **ruff**: Fast Python linter and formatter (replaces flake8, black, isort, etc.)
- **ty**: Fast type checker from Astral
- **pre-commit**: Automated code quality checks before commits
- **hatchling**: Modern Python build backend

### Pre-commit Hooks

Pre-commit hooks automatically run on every commit to ensure code quality:

- `ruff check --fix`: Auto-fix linting issues
- `ruff format`: Format code
- `ty`: Check type annotations

To run hooks manually:

```bash
uv run pre-commit run --all-files
```

### Making Changes

1. Make your changes to the code
2. Run formatting and linting: `uv run ruff check --fix && uv run ruff format`
3. Run type checking: `uv run ty`
4. Test your changes
5. Commit (pre-commit hooks will run automatically)

## API

### check_syntax

Checks PineScript syntax using TradingView's API.

**Parameters:**
- `pine_code` (str): The PineScript code to check

**Returns:**
- `dict`: Dictionary containing check results with keys:
  - `success` (bool): Whether the check succeeded
  - `error` (str, optional): Error message if check failed
  - `errors` (list): List of syntax errors
  - `result` (dict, optional): Parsed result from TradingView

## Example

**Input:**
```pinescript
//@version=5
strategy("Test")
plot(close)
```

**Output:**
```json
{
  "success": true,
  "result": {
    "variables": [],
    "functions": [],
    "types": [],
    "enums": []
  }
}
```

## Project Structure

```
pinescript_syntax_checker/
├── .pre-commit-config.yaml          # Pre-commit hooks configuration
├── pyproject.toml                   # Project configuration and dependencies
├── README.md                        # This file
├── LICENSE                          # MIT License
└── pinescript_syntax_checker/       # Main package
    ├── __init__.py                  # Package initialization
    ├── pinescript_checker.py        # CLI and checker implementation (executable)
    └── server.py                    # MCP server implementation
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with proper type hints and documentation
4. Ensure all tests pass and code is formatted
5. Submit a pull request

## License

MIT License - see LICENSE file for details
