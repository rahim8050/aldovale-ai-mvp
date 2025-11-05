import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.core.models import Client
import hashlib
from rest_framework_simplejwt.tokens import AccessToken


@pytest.mark.django_db
def test_session_create() -> None:
    raw_api_key = "valid_api_key_123"
    hashed_key = hashlib.sha256(raw_api_key.encode()).hexdigest()
    client_obj = Client.objects.create(name="Test Co", api_key_hash=hashed_key)

    # Generate valid JWT token for this client
    token = AccessToken()
    token["client_id"] = str(client_obj.id)
    token["name"] = client_obj.name
    jwt_token = str(token)

    api_client = APIClient()
    api_client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

    url = reverse("session-create")
    payload = {"client_id": str(client_obj.id)}

    response = api_client.post(url, payload, format="json")

    assert response.status_code == 201, response.content
    data = response.json()
    assert "data" in data, response.content
    assert "session_id" in data["data"], response.content
