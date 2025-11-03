import pytest
from typing import Any
from django.urls import reverse
from rest_framework.test import APIClient
from apps.core.models import Client


@pytest.mark.django_db  # type: ignore[misc]
def test_session_create(api_client_with_auth: APIClient) -> None:
    """
    Test creating a session for a client returns a valid session ID and JWT token.
    """
    client_obj: Client = Client.objects.create(name="Test Co", api_key_hash="hash")
    url: str = reverse("session-create")
    payload: dict[str, Any] = {"client_id": str(client_obj.id)}

    response = api_client_with_auth.post(url, payload, format="json")

    assert response.status_code == 200, response.content
    data: dict[str, Any] = response.json()

    assert "session_id" in data, "Missing session_id in response"
    assert "jwt" in data, "Missing jwt in response"
    assert isinstance(data["jwt"], str)
    assert isinstance(data["session_id"], str)
