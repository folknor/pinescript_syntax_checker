# PineScript Syntax Checker MCP Server

A Model Context Protocol (MCP) server and CLI script for checking PineScript syntax using TradingView's API. Forked from https://github.com/erevus-cn/pinescript_syntax_checker (thanks to erevus for the original work).

## Features

- Check PineScript syntax using TradingView's official API
- MCP-compatible server with httpx for async HTTP requests
- Option to run checks from the CLI (can be run by Codex and is much faster)
- CLI output drops the unused `scopes` array by default to save context/tokens (`--full-response` keeps it)
- Detailed error reporting with line and column information

## Quick Start

Use the `pinescript_syntax_checker` CLI or the MCP server inside OpenAI Codex.

### Run as CLI script
Simpler and faster than MCP. Use it manually, or have Codex/Claude/Gemini call it in the console after edits.

```bash
# check usage
python3 pinescript_syntax_checker/pinescript_checker.py --help

# run a check on a file
python3 pinescript_syntax_checker/pinescript_checker.py pinescript-file.pine --pretty
```
### Run as MCP server
Build the pip package using `pyproject.toml`, then run:

```bash
# make sure you are in project dir
cd pinescript_syntax_checker

# install build package
python -m pip install build

# build pip module, which will create package and put it into dist/ dir
python -m build

# install package you just built
python -m pip install dist/pinescript_syntax_checker-0.1.0-py3-none-any.whl

# add it to codex
codex mcp add pinescript-syntax-checker -- pinescript-syntax-checker

# verify it was added
codex mcp list
```

To undo the MCP setup:

```bash
# remove from codex
codex mcp remove pinescript-syntax-checker

# verify that it was removed
codex mcp list

# uninstall pip package
python -m pip uninstall dist/pinescript_syntax_checker-0.1.0-py3-none-any.whl

# remove build artifacts (make sure you are in project folder)
rm -rf dist build *.egg-info
```
## API

### check_syntax

Checks PineScript syntax using TradingView's API.

**Parameters:**
- `pine_code` (str): The PineScript code to check

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
    "enums": [],
    "scopes": []
  }
}
```

## License

MIT License
