import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.core.models import Client, Session


@pytest.mark.django_db  # type: ignore[misc]
def test_chat_message_flow() -> None:
    client_obj = Client.objects.create(name="Test Co", api_key_hash="hash")
    session = Session.objects.create(client=client_obj, jwt_jti="jti-1")

    api = APIClient()
    url = reverse("chat-message")
    payload = {"session_id": str(session.id), "message": "hello"}

    response = api.post(url, payload, format="json")

    assert response.status_code == 200, response.content
    data = response.json()

    # confirm structure + behavior
    assert "reply" in data
    assert isinstance(data["reply"], str)
    assert data["reply"].startswith("Echo:"), f"Unexpected reply: {data['reply']}"
