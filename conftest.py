import os
import django
import pytest
from typing import Any
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


def pytest_configure() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "aldovale.settings")
    django.setup()


@pytest.fixture
def user(db: Any) -> User:
    """
    Creates and returns a test user.
    """
    test_password = os.getenv("TEST_USER_PASSWORD", "default_test_password")
    return User.objects.create_user(username="testuser", password=test_password)


@pytest.fixture
def api_client_with_auth(user: User) -> APIClient:
    """
    Returns an APIClient instance authenticated with JWT for the given user.
    """
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")
    return client
