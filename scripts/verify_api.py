#!/usr/bin/env python3
"""Verify a real GET /health response and optionally save JSON evidence."""

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, urlunsplit
from urllib.request import Request, urlopen

EXPECTED = {
    "status": "ok", "service": "CloudMate",
    "message": "AWS Lambda is working", "week": 2,
}


def health_url(value: str) -> str:
    parts = urlsplit(value)
    local = parts.hostname in {"localhost", "127.0.0.1", "::1"}
    if not parts.hostname or parts.scheme not in {"http", "https"}:
        raise ValueError("Provide an HTTPS API base URL or /health URL")
    if parts.scheme != "https" and not local:
        raise ValueError("HTTP is allowed only for localhost smoke tests")
    if parts.username or parts.password or parts.query or parts.fragment:
        raise ValueError("Do not include credentials, query strings or fragments")
    path = parts.path.rstrip("/")
    if not path.endswith("/health"):
        path += "/health"
    return urlunsplit((parts.scheme, parts.netloc, path, "", ""))


def verify(url: str, timeout: float = 10) -> dict:
    result = {
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "url": url,
        "target": "local" if urlsplit(url).hostname in {"localhost", "127.0.0.1", "::1"} else "remote",
        "passed": False,
    }
    request = Request(url, headers={"Accept": "application/json"}, method="GET")
    try:
        with urlopen(request, timeout=timeout) as response:
            result["http_status"] = response.status
            result["content_type"] = response.headers.get_content_type()
            result["response"] = json.loads(response.read(65536).decode("utf-8"))
        result["passed"] = (
            result["http_status"] == 200
            and result["content_type"] == "application/json"
            and result["response"] == EXPECTED
        )
        if not result["passed"]:
            result["error"] = "Unexpected HTTP status, Content-Type or JSON response"
    except HTTPError as error:
        result.update(http_status=error.code, error="HTTP request failed")
    except (URLError, TimeoutError, OSError, ValueError) as error:
        result["error"] = type(error).__name__
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Deployed API base URL or full /health URL")
    parser.add_argument("--timeout", type=float, default=10)
    parser.add_argument("--output", type=Path, help="Optional reviewed evidence JSON path")
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error("--timeout must be positive")
    try:
        url = health_url(args.url)
    except ValueError as error:
        parser.error(str(error))
    result = verify(url, args.timeout)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    print(rendered, end="")
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
