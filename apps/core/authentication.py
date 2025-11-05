from typing import Any
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token
from django.contrib.auth.models import AnonymousUser
from apps.core.models import Client


class ClientJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token: Token) -> Any:
        client_id = validated_token.get("client_id")
        if client_id is None:
            return AnonymousUser()

        try:
            return Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return AnonymousUser()
