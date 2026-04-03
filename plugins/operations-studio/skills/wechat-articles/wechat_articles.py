#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx",
# ]
# ///
"""
WeChat Official Account Articles API Client.

Provides three capabilities:
1. Get today's publishing status of an account
2. Get historical article list with pagination
3. Convert short article links to long links (with biz extraction)

Requires JZL_API_KEY environment variable.
API rate limit: max 5 requests/second.
"""

import argparse
import json
import os
import sys
import time
from urllib.parse import parse_qs, urlparse

import httpx

BASE_URL = "https://www.dajiala.com/fbmain/monitor/v3"
QPS_LIMIT = 5
REQUEST_INTERVAL = 1.0 / QPS_LIMIT  # 0.2s between requests

_last_request_time = 0.0


def _get_api_key() -> str:
    key = os.environ.get("JZL_API_KEY")
    if not key:
        print("Error: JZL_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    return key


def _rate_limit():
    """Enforce QPS limit by sleeping if needed."""
    global _last_request_time
    now = time.monotonic()
    elapsed = now - _last_request_time
    if elapsed < REQUEST_INTERVAL:
        time.sleep(REQUEST_INTERVAL - elapsed)
    _last_request_time = time.monotonic()


def _post(endpoint: str, payload: dict) -> dict:
    """Send POST request with rate limiting and error handling."""
    _rate_limit()
    url = f"{BASE_URL}/{endpoint}"
    try:
        with httpx.Client(timeout=30) as client:
            resp = client.post(url, json=payload)
            resp.raise_for_status()
            return resp.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e.response.status_code} - {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except httpx.RequestError as e:
        print(f"Request error: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Failed to decode JSON response from {url}", file=sys.stderr)
        sys.exit(1)


def _build_account_params(biz: str | None, name: str | None, url: str | None) -> dict:
    """Build account identifier params; at least one of biz/name/url is required."""
    params = {}
    if biz:
        params["biz"] = biz
    if name:
        params["name"] = name
    if url:
        params["url"] = url
    if not params:
        print("Error: at least one of --biz, --name, or --url is required.", file=sys.stderr)
        sys.exit(1)
    return params


def _extract_biz_from_long_url(long_url: str) -> str | None:
    """Extract __biz parameter from a long WeChat article URL."""
    try:
        parsed = urlparse(long_url)
        qs = parse_qs(parsed.query)
        biz_list = qs.get("__biz", [])
        return biz_list[0] if biz_list else None
    except Exception:
        return None


def cmd_today(args):
    """Get today's publishing status."""
    key = _get_api_key()
    payload = {
        **_build_account_params(args.biz, args.name, args.url),
        "key": key,
        "verifycode": "",
    }
    result = _post("post_condition", payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_history(args):
    """Get historical article list with pagination."""
    key = _get_api_key()
    payload = {
        **_build_account_params(args.biz, args.name, args.url),
        "page": args.page,
        "key": key,
        "verifycode": "",
    }
    result = _post("post_history", payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_short2long(args):
    """Convert short link to long link and optionally extract biz."""
    key = _get_api_key()
    payload = {
        "link": args.link,
        "key": key,
        "verifycode": "",
    }
    result = _post("link/short2long", payload)

    # Extract biz from the long URL if conversion succeeded
    if result.get("code") == 0 and result.get("long_url"):
        biz = _extract_biz_from_long_url(result["long_url"])
        if biz:
            result["extracted_biz"] = biz

    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(
        description="WeChat Official Account Articles API Client"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- today ---
    p_today = subparsers.add_parser("today", help="Get today's publishing status")
    p_today.add_argument("--biz", help="Account biz (base64 encoded)")
    p_today.add_argument("--name", help="Account name or wxid")
    p_today.add_argument("--url", help="Any article URL from the account")
    p_today.set_defaults(func=cmd_today)

    # --- history ---
    p_hist = subparsers.add_parser("history", help="Get historical article list")
    p_hist.add_argument("--biz", help="Account biz (base64 encoded)")
    p_hist.add_argument("--name", help="Account name or wxid")
    p_hist.add_argument("--url", help="Any article URL from the account")
    p_hist.add_argument("--page", type=int, default=1, help="Page number (default: 1)")
    p_hist.set_defaults(func=cmd_history)

    # --- short2long ---
    p_s2l = subparsers.add_parser("short2long", help="Convert short link to long link")
    p_s2l.add_argument("link", help="WeChat article short link")
    p_s2l.set_defaults(func=cmd_short2long)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
