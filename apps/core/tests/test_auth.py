import hashlib
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.core.models import Client
from rest_framework_simplejwt.tokens import AccessToken
from apps.core.utils import generate_jwt


def get_access_token_for_client(client: Client) -> str:
    token = AccessToken()
    token["client_id"] = str(client.id)
    token["name"] = client.name
    # token.set_exp()  # SimpleJWT sets default expiration, so you can skip this unless you want custom expiry
    return str(token)


@pytest.mark.django_db
def test_token_exchange_success() -> None:
    raw_api_key = "valid_api_key_123"
    hashed_key = hashlib.sha256(raw_api_key.encode()).hexdigest()
    client_obj = Client.objects.create(name="Test Co", api_key_hash=hashed_key)

    jwt_token = get_access_token_for_client(client_obj)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

    response = client.post(
        reverse("token-exchange"),
        {"api_key": raw_api_key},
        format="json",
    )

    assert response.status_code == 200, response.content
    response_data = response.json()
    assert "jwt" in response_data.get("data", {}), response.content


@pytest.mark.django_db
def test_session_create() -> None:
    raw_api_key = "valid_api_key_123"
    hashed_key = hashlib.sha256(raw_api_key.encode()).hexdigest()
    client_obj = Client.objects.create(name="Test Co", api_key_hash=hashed_key)

    jwt_token = generate_jwt(client_obj)

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {jwt_token}")

    url = reverse("session-create")
    payload = {"client_id": str(client_obj.id)}

    response = client.post(url, payload, format="json")

    assert response.status_code == 201, response.content

    response_data = response.json()
    assert "data" in response_data, response.content
    assert "session_id" in response_data["data"], response.content
    assert response_data["data"]["client"] == "Test Co"
