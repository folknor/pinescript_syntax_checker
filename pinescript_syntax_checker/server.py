#!/usr/bin/env python3
"""MCP Server for PineScript syntax checking."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from .pinescript_checker import PineScriptChecker

app = FastMCP("pinescript-syntax-checker")


@app.tool()
async def check_syntax(pine_code: str) -> dict[str, Any]:
    """Check PineScript syntax using TradingView's API.

    Args:
        pine_code: PineScript code to check

    Returns:
        Dictionary containing syntax check results with keys:
            - success (bool): Whether the check succeeded
            - error (str, optional): Error message if check failed
            - errors (list): List of syntax errors
            - result (dict, optional): Parsed result from TradingView
    """
    checker = PineScriptChecker()

    try:
        return await checker.check_syntax(pine_code)
    except Exception as e:
        return {
            "success": False,
            "error": f"Check failed: {e!s}",
            "errors": [],
        }


def main() -> None:
    """Entry point for the MCP server."""
    app.run()


if __name__ == "__main__":
    main()
