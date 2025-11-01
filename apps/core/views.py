from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Client, Session, Conversation
from .serializers import (
    SessionCreateSerializer,
    IngestSerializer,
)
import jwt
import os
import uuid


# Simple token exchange endpoint (dev-only)
class TokenExchangeView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        api_key = request.data.get("api_key")
        if not api_key:
            return Response(
                {"detail": "api_key required"}, status=status.HTTP_400_BAD_REQUEST
            )
        # In prod: verify hashed api_key against DB
        payload = {"jti": str(uuid.uuid4())}
        token = jwt.encode(
            payload, os.getenv("SECRET_KEY", "replace-me"), algorithm="HS256"
        )
        return Response({"jwt": token})


class SessionCreateView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SessionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client_id = serializer.validated_data["client_id"]
        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            return Response(
                {"detail": "client not found"}, status=status.HTTP_404_NOT_FOUND
            )
        session = Session.objects.create(client=client, jwt_jti=str(uuid.uuid4()))
        return Response({"session_id": str(session.id), "jwt": "dev-jwt-placeholder"})


class ChatMessageView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        session_id = request.data.get("session_id")
        message = request.data.get("message")
        if not session_id or not message:
            return Response(
                {"detail": "session_id and message required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            session = Session.objects.get(id=session_id)
        except Session.DoesNotExist:
            return Response(
                {"detail": "session not found"}, status=status.HTTP_404_NOT_FOUND
            )
        # Simple echo / placeholder LLM call
        conv = Conversation.objects.create(
            session=session,
            client=session.client,
            user_message=message,
            bot_reply=f"Echo: {message}",
        )
        return Response(
            {"reply": conv.bot_reply, "sources": [], "ticket_created": False}
        )


class AdminIngestView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = IngestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # store file and enqueue ingestion job in real product
        return Response({"detail": "file received"}, status=status.HTTP_202_ACCEPTED)
