import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from app import app


class ChatbotTests(unittest.TestCase):
    def setUp(self):
        app.config.update(TESTING=True)
        self.client = app.test_client()

    @patch.dict(os.environ, {"GROQ_API_KEY": "dummy"}, clear=False)
    @patch("app.get_client")
    def test_chat_returns_reply(self, mock_get_client):
        mock_client = SimpleNamespace()
        mock_client.chat = SimpleNamespace(
            completions=SimpleNamespace(
                create=lambda **kwargs: SimpleNamespace(
                    choices=[SimpleNamespace(message=SimpleNamespace(content="Hello from the bot"))]
                )
            )
        )
        mock_get_client.return_value = mock_client

        response = self.client.post("/api/chat", json={"message": "Hi there"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["reply"], "Hello from the bot")


if __name__ == "__main__":
    unittest.main()
