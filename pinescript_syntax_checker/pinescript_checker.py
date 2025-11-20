import httpx
import json
import argparse
from pathlib import Path
import sys
import asyncio

class PineScriptChecker:
    def __init__(self, username="admin"):
        self.username = username
        self.api_url = f"https://pine-facade.tradingview.com/pine-facade/translate_light?user_name={username}&v=3"
        self.headers = {
            'Referer': 'https://www.tradingview.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'DNT': '1',
        }

    async def check_syntax(self, pine_code):
        """
        Check PineScript code syntax
        
        Args:
            pine_code (str): PineScript source code
            
        Returns:
            dict: Dictionary containing check results
        """
        try:
            # Build multipart form data
            files = self._build_multipart_data(pine_code)
            
            # Send request using httpx
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.api_url,
                    files=files,
                    headers=self.headers,
                    timeout=10.0
                )
                # Parse response
                result = response.json()
                return result
            
        except httpx.RequestError as e:
            return {
                'success': False,
                'error': f'Network request failed: {str(e)}',
                'errors': []
            }

    def _build_multipart_data(self, pine_code, boundary=None):
        """Build multipart form data - using standard format"""
        # Using httpx files parameter is more reliable
        return {
            'source': (None, pine_code)
        }

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Check PineScript syntax using TradingView's public endpoint. "
            "Example: python3 pinescript_checker.py my_script.pine --pretty"
        )
    )
    parser.add_argument(
        "path",
        type=Path,
        help="Path to the PineScript file to validate"
    )
    parser.add_argument(
        "--username",
        default="admin",
        help="TradingView username used for the request (default: admin)"
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output"
    )
    parser.add_argument(
        "--full-response",
        action="store_true",
        help="Return the raw TradingView payload (including rarely used 'scopes'). "
        "By default, unused sections are omitted to keep output concise.",
    )
    args = parser.parse_args()

    try:
        pine_code = args.path.read_text(encoding="utf-8")
    except OSError as exc:
        print(json.dumps({
            'success': False,
            'error': f'Unable to read file {args.path}: {exc}',
            'errors': []
        }))
        sys.exit(1)

    checker = PineScriptChecker(username=args.username)
    result = asyncio.run(checker.check_syntax(pine_code))

    if not args.full_response:
        payload = result.get("result")
        if isinstance(payload, dict):
            payload.pop("scopes", None)

    if args.pretty:
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))

    if not result.get('success', True):
        sys.exit(1)

if __name__ == "__main__":
    main()

