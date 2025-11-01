import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.core.models import Client, Session


@pytest.mark.django_db
def test_chat_message_flow():
    c = Client.objects.create(name="Test Co", api_key_hash="hash")
    s = Session.objects.create(client=c, jwt_jti="jti-1")
    api = APIClient()
    resp = api.post(
        reverse("chat-message"),
        {"session_id": str(s.id), "message": "hello"},
        format="json",
    )
    assert resp.status_code == 200
    json = resp.json()
    assert "reply" in json and json["reply"].startswith("Echo:")
