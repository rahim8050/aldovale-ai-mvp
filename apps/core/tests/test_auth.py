import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db  # type: ignore[misc]
def test_token_exchange_success() -> None:
    api = APIClient()
    response = api.post(reverse("token-exchange"), {"api_key": "fake"}, format="json")

    assert response.status_code == 200, response.content
    data = response.json()
    assert "jwt" in data
    assert isinstance(data["jwt"], str)
