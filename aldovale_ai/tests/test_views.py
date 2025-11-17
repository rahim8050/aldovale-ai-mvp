import os
import pytest
from rest_framework.test import APITestCase
from django.test import override_settings
from unittest.mock import patch, MagicMock
import jwt
from datetime import timedelta
from django.utils import timezone


# Load a dummy secret from the environment with a fallback
TEST_JWT_SECRET = os.environ.get("TEST_JWT_SECRET_KEY", "dummy-test-key")


@pytest.mark.django_db
@override_settings(EXPECTED_API_KEY="valid-api-key", JWT_SECRET_KEY=TEST_JWT_SECRET)
class TestAuthToken(APITestCase):
    def test_token_obtain_success(self) -> None:
        response = self.client.post(
            "/api/v1/aldovale_ai/auth/token/",
            {"api_key": "valid-api-key"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("jwt", response.json())

    def test_token_obtain_failure(self) -> None:
        response = self.client.post(
            "/api/v1/aldovale_ai/auth/token/", {"api_key": "invalid"}, format="json"
        )
        self.assertEqual(response.status_code, 401)


@pytest.mark.django_db
@override_settings(
    OLLAMA_BASE_URL="http://localhost:11434",
    OLLAMA_MODEL="test-model",
    JWT_SECRET_KEY=TEST_JWT_SECRET,
)
class TestChatSession(APITestCase):
    @patch("aldovale_ai.clients.OllamaClient.generate", return_value="response")
    def test_chat_session_success(self, mock_generate: MagicMock) -> None:
        now = timezone.now()
        payload = {
            "exp": int((now + timedelta(hours=1)).timestamp()),
            "iat": int(now.timestamp()),
            "sub": "service-api",
        }

        token = jwt.encode(payload, TEST_JWT_SECRET, algorithm="HS256")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.post(
            "/api/v1/aldovale_ai/chat/session/", {"message": "Hello"}, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["response"], "response")
        mock_generate.assert_called_once()
