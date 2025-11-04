from rest_framework import serializers
from typing import Any
from .models import Client, Conversation


class ClientSerializer(serializers.ModelSerializer[Client]):
    class Meta:
        model = Client
        fields = ["id", "name", "webhook_url", "config"]


class SessionCreateSerializer(serializers.Serializer[Any]):
    client_id = serializers.UUIDField()


class ConversationSerializer(serializers.ModelSerializer[Conversation]):
    class Meta:
        model = Conversation
        fields = [
            "id",
            "session",
            "client",
            "user_message",
            "bot_reply",
            "sources",
            "created_at",
        ]


class IngestSerializer(serializers.Serializer[Any]):
    file = serializers.FileField()
