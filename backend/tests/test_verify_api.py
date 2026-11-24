"""Ensure endpoint evidence fails closed when HTTP or JSON is incorrect."""

import json
from email.message import Message
import unittest
from unittest.mock import MagicMock, patch
from urllib.error import HTTPError, URLError

from scripts import verify_api


class VerifyApiTests(unittest.TestCase):
    def test_url_normalization(self):
        self.assertEqual(verify_api.health_url("https://example.com/"), "https://example.com/health")
        self.assertEqual(verify_api.health_url("https://example.com/dev/health"), "https://example.com/dev/health")

    def test_unsafe_urls_are_rejected(self):
        for value in ("http://example.com", "https://user:secret@example.com", "https://example.com?token=secret", "example.com"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                verify_api.health_url(value)

    def test_response_contract(self):
        for status, content_type, payload, expected in (
            (200, "application/json", verify_api.EXPECTED, True),
            (201, "application/json", verify_api.EXPECTED, False),
            (200, "text/html", verify_api.EXPECTED, False),
            (200, "application/json", {"status": "ok"}, False),
        ):
            with self.subTest(status=status, content_type=content_type, payload=payload):
                response = MagicMock()
                response.status = status
                response.headers = Message()
                response.headers["Content-Type"] = content_type
                response.read.return_value = json.dumps(payload).encode()
                response.__enter__.return_value = response
                with patch.object(verify_api, "urlopen", return_value=response):
                    self.assertIs(verify_api.verify("https://example.com/health")["passed"], expected)

    def test_network_and_http_errors_fail(self):
        for error in (URLError("offline"), HTTPError("https://example.com/health", 403, "Forbidden", {}, None)):
            with self.subTest(error=type(error).__name__), patch.object(verify_api, "urlopen", side_effect=error):
                self.assertIs(verify_api.verify("https://example.com/health")["passed"], False)


if __name__ == "__main__":
    unittest.main()
