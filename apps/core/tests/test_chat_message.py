import pytest
from typing import Any
from django.urls import reverse
from rest_framework.test import APIClient
from apps.core.models import Client, Session


@pytest.mark.django_db  # type: ignore[misc]
def test_chat_message_flow(api_client_with_auth: APIClient) -> None:
    """
    Tests the chat message flow endpoint with authenticated client.

    Creates Client and Session instances, then sends a chat message
    and verifies the response structure and content.
    """
    client_obj: Client = Client.objects.create(name="Test Co", api_key_hash="hash")
    session: Session = Session.objects.create(client=client_obj, jwt_jti="jti-1")

    url: str = reverse("chat-message")
    payload: dict[str, Any] = {"session_id": str(session.id), "message": "hello"}

    response = api_client_with_auth.post(url, payload, format="json")

    assert response.status_code == 200, response.content
    data: dict[str, Any] = response.json()

    # Adjust for nested structure under "data"
    assert "data" in data, f"Missing 'data' key in response: {data}"
    assert "reply" in data["data"], f"Missing 'reply' key in data: {data['data']}"
    assert isinstance(data["data"]["reply"], str)
    assert data["data"]["reply"].startswith(
        "Echo:"
    ), f"Unexpected reply: {data['data']['reply']}"
