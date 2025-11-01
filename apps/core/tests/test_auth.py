import pytest
from django.urls import reverse
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_token_exchange():
    client = APIClient()
    resp = client.post(reverse('token-exchange'), {'api_key': 'fake'}, format='json')
    assert resp.status_code == 200
    assert 'jwt' in resp.json()
