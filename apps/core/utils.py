from typing import Any
import jwt
import uuid
import os
from apps.core.models import Client


def generate_jwt(client: Client | None = None) -> str:
    secret = os.getenv("SECRET_KEY", "replace-me")
    payload: dict[str, Any] = {}

    if client is not None:
        payload = {
            "client_id": str(client.id),
            "name": client.name,
            # add other claims as needed
        }

    payload["jti"] = str(uuid.uuid4())

    token = jwt.encode(payload, secret, algorithm="HS256")
    return token
