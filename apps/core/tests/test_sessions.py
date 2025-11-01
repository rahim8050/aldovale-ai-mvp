import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from apps.core.models import Client

@pytest.mark.django_db
def test_session_create(client):
    c = Client.objects.create(name='Test Co', api_key_hash='hash')
    api = APIClient()
    resp = api.post(reverse('session-create'), {'client_id': str(c.id)}, format='json')
    assert resp.status_code == 200
    data = resp.json()
    assert 'session_id' in data and 'jwt' in data
