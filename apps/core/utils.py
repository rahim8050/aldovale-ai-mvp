from typing import Optional
from datetime import timedelta
from rest_framework_simplejwt.tokens import AccessToken
from apps.core.models import Client


def generate_jwt(client: Optional[Client] = None) -> str:
    token = AccessToken()
    token.set_exp(lifetime=timedelta(minutes=5))  # set expiry as needed

    if client:
        token["client_id"] = str(client.id)
        token["name"] = client.name
        # add other custom claims here if needed

    return str(token)
