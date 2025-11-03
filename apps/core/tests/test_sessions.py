import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.core.models import Client


@pytest.mark.django_db  # type: ignore[misc]
def test_session_create() -> None:
    client_obj = Client.objects.create(name="Test Co", api_key_hash="hash")
    api = APIClient()
    url = reverse("session-create")
    payload = {"client_id": str(client_obj.id)}

    response = api.post(url, payload, format="json")

    assert response.status_code == 200, response.content
    data = response.json()

    assert "session_id" in data, "Missing session_id in response"
    assert "jwt" in data, "Missing jwt in response"
    assert isinstance(data["jwt"], str)
    assert isinstance(data["session_id"], str)
