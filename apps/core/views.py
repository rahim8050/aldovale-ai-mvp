from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from apps.core.models import Client, Session
from apps.core.serializers import SessionCreateSerializer, IngestSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.decorators import permission_classes
import hashlib
import uuid
from typing import Dict, Any


def generate_test_jwt_for_client(client: Client) -> str:
    token = AccessToken()
    # Custom claims — adapt as needed
    token["client_id"] = str(client.id)
    token["name"] = client.name
    return str(token)


@api_view(["POST"])
@permission_classes([AllowAny])
def token_exchange(request: Request) -> Response:
    api_key = request.data.get("api_key")
    if not api_key:
        return Response(
            {"detail": "Missing API key."}, status=status.HTTP_400_BAD_REQUEST
        )

    hashed_key = hashlib.sha256(api_key.encode()).hexdigest()
    client = Client.objects.filter(api_key_hash=hashed_key).first()
    if not client:
        return Response(
            {"detail": "Invalid API key."}, status=status.HTTP_401_UNAUTHORIZED
        )

    # Generate JWT token using SimpleJWT AccessToken or your generate_jwt util
    # For simplicity:
    from rest_framework_simplejwt.tokens import AccessToken

    token = AccessToken()
    token["client_id"] = str(client.id)
    token["name"] = client.name

    return Response({"jwt": str(token)}, status=status.HTTP_200_OK)


@api_view(["POST"])
def session_create(request: Request) -> Response:
    serializer = SessionCreateSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    validated_data: Dict[str, Any] = serializer.save()
    client_id = validated_data["client_id"]

    try:
        client = Client.objects.get(id=client_id)
    except Client.DoesNotExist:
        return Response(
            {"detail": "Client does not exist"}, status=status.HTTP_400_BAD_REQUEST
        )

    jwt_jti = str(uuid.uuid4())
    session = Session.objects.create(client=client, jwt_jti=jwt_jti)

    return Response(
        {"session_id": str(session.id), "client": session.client.name},
        status=status.HTTP_201_CREATED,
    )


@api_view(["POST"])
def chat_message(request: Request) -> Response:
    session_id = request.data.get("session_id")
    message = request.data.get("message")

    if not session_id or not message:
        return Response(
            {"detail": "Missing session_id or message."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        session = Session.objects.get(id=session_id)
    except Session.DoesNotExist:
        return Response(
            {"detail": "Session not found."}, status=status.HTTP_404_NOT_FOUND
        )

    reply = f"Echo: {message}"
    return Response(
        {"reply": reply, "session": str(session.id)}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
def ingest_data(request: Request) -> Response:
    serializer = IngestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response({"status": "success"}, status=status.HTTP_201_CREATED)
