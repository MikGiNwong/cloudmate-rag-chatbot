"""Response contract and failure-path tests; no AWS credentials required."""

import json
import unittest
from unittest.mock import patch

from backend.health import app


def http_event(method="GET", path="/health"):
    return {
        "version": "2.0",
        "rawPath": path,
        "requestContext": {"http": {"method": method, "path": path}},
    }


class HealthTests(unittest.TestCase):
    def test_get_health_returns_exact_contract(self):
        result = app.lambda_handler(http_event(), None)
        self.assertEqual(result["statusCode"], 200)
        self.assertEqual(json.loads(result["body"]), {
            "status": "ok", "service": "CloudMate",
            "message": "AWS Lambda is working",
        })
        self.assertEqual(result["headers"]["Content-Type"], "application/json; charset=utf-8")
        self.assertEqual(result["headers"]["Cache-Control"], "no-store")
        self.assertIs(result["isBase64Encoded"], False)

    def test_unknown_path_returns_404(self):
        self.assertEqual(app.lambda_handler(http_event(path="/chat"), None)["statusCode"], 404)

    def test_other_methods_return_405(self):
        for method in ("POST", "PUT", "DELETE", "HEAD", "OPTIONS"):
            with self.subTest(method=method):
                result = app.lambda_handler(http_event(method=method), None)
                self.assertEqual(result["statusCode"], 405)
                self.assertEqual(result["headers"]["Allow"], "GET")

    def test_malformed_events_return_400(self):
        for event in (None, [], {}, {"requestContext": None}, {"requestContext": {"http": []}}):
            with self.subTest(event=event):
                self.assertEqual(app.lambda_handler(event, None)["statusCode"], 400)

    def test_exception_returns_safe_json_and_safe_log(self):
        with patch.object(app, "health_payload", side_effect=RuntimeError("private-token-value")):
            with self.assertLogs(app.LOGGER, level="ERROR") as logs:
                result = app.lambda_handler(http_event(), None)
        self.assertEqual(result["statusCode"], 500)
        self.assertEqual(json.loads(result["body"]), {
            "status": "error", "message": "Internal server error",
        })
        self.assertNotIn("private-token-value", result["body"] + str(logs.output))

    def test_request_and_context_are_not_logged(self):
        event = http_event()
        event["headers"] = {"Authorization": "private-token-value"}
        event["body"] = "private-user-question"
        with self.assertLogs(app.LOGGER, level="INFO") as logs:
            result = app.lambda_handler(event, {"identity": "private-user-id"})
        self.assertEqual(result["statusCode"], 200)
        for secret in ("private-token-value", "private-user-question", "private-user-id"):
            self.assertNotIn(secret, str(logs.output))


if __name__ == "__main__":
    unittest.main()
