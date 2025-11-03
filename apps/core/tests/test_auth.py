import pytest
from typing import Any
from django.urls import reverse
from rest_framework.test import APIClient
from apps.core.models import Client
import hashlib


@pytest.mark.django_db  # type: ignore[misc]
def test_token_exchange_success(api_client: APIClient) -> None:
    """
    Test that token exchange endpoint returns a valid JWT token
    when provided a valid API key.
    """
    # Arrange: create a Client with a hashed API key
    raw_api_key = "valid_api_key_123"
    hashed_key = hashlib.sha256(raw_api_key.encode()).hexdigest()
    Client.objects.create(name="Test Co", api_key_hash=hashed_key)

    # Act: call the token-exchange endpoint with the raw API key
    response = api_client.post(
        reverse("token-exchange"), {"api_key": raw_api_key}, format="json"
    )

    # Assert: successful response with JWT token
    assert response.status_code == 200, response.content
    data: dict[str, Any] = response.json()
    assert "jwt" in data
    assert isinstance(data["jwt"], str)
