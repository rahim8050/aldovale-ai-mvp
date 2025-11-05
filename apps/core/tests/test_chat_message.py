import pytest
from typing import Any, Dict
from django.urls import reverse
from rest_framework.test import APIClient
from apps.core.models import Client, Session
from apps.core.utils import generate_jwt  # assuming you have this util
import hashlib


@pytest.fixture
def api_client_with_auth() -> APIClient:
    """
    Returns an APIClient instance with JWT authentication
    for a newly created Client.
    """
    raw_api_key = "valid_api_key_123"
    hashed_key = hashlib.sha256(raw_api_key.encode()).hexdigest()
    client_obj = Client.objects.create(name="Test Co", api_key_hash=hashed_key)

    jwt_token = generate_jwt(client_obj)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")
    return client


@pytest.mark.django_db
def test_chat_message_flow(api_client_with_auth: APIClient) -> None:
    """
    Tests the chat message flow endpoint with authenticated client.
    """
    # Retrieve the client tied to the authenticated API client (via JWT)
    # If your fixture creates and returns the APIClient only,
    # you may want to create Client and Session here explicitly instead.

    # For safety, create a client here as well:
    client_obj = Client.objects.first()
    assert client_obj is not None

    session: Session = Session.objects.create(client=client_obj, jwt_jti="jti-1")

    url: str = reverse("chat-message")
    payload: Dict[str, Any] = {"session_id": str(session.id), "message": "hello"}

    response = api_client_with_auth.post(url, payload, format="json")

    assert response.status_code == 200, response.content
    data: Dict[str, Any] = response.json()

    assert "data" in data, f"Missing 'data' key in response: {data}"
    assert "reply" in data["data"], f"Missing 'reply' key in data: {data['data']}"
    assert isinstance(data["data"]["reply"], str)
    assert data["data"]["reply"].startswith(
        "Echo:"
    ), f"Unexpected reply: {data['data']['reply']}"
