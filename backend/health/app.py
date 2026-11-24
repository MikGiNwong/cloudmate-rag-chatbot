"""CloudMate week 2 health endpoint for API Gateway HTTP API payload v2."""

import json
import logging
from typing import Any

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def health_payload() -> dict[str, str | int]:
    """Return the public response contract without accessing AWS services."""
    return {
        "status": "ok",
        "service": "CloudMate",
        "message": "AWS Lambda is working",
        "week": 2,
    }


def _response(status_code: int, payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json; charset=utf-8",
            "Cache-Control": "no-store",
        },
        "isBase64Encoded": False,
        "body": json.dumps(payload, ensure_ascii=False),
    }


def lambda_handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Handle only GET /health; keep events and exception details out of logs."""
    try:
        if not isinstance(event, dict):
            return _response(400, {"message": "Invalid request"})
        request_context = event.get("requestContext")
        if not isinstance(request_context, dict):
            return _response(400, {"message": "Invalid request"})
        http = request_context.get("http")
        if not isinstance(http, dict):
            return _response(400, {"message": "Invalid request"})
        if event.get("rawPath") != "/health":
            return _response(404, {"message": "Not found"})
        if http.get("method") != "GET":
            response = _response(405, {"message": "Method not allowed"})
            response["headers"]["Allow"] = "GET"
            return response

        response = _response(200, health_payload())
        LOGGER.info("health_check status=ok week=2")
        return response
    except Exception:
        # Never log the event, context, exception text, tokens or personal data.
        LOGGER.error("health_check status=error week=2")
        return _response(500, {"status": "error", "message": "Internal server error"})
