from rest_framework import serializers
from typing import Any, Dict
from .models import Client, Conversation


class ClientSerializer(serializers.ModelSerializer[Client]):
    class Meta:
        model = Client
        fields = ["id", "name", "webhook_url", "config"]


class SessionCreateSerializer(serializers.Serializer[Dict[str, Any]]):
    client_id = serializers.UUIDField()

    # Just validate input, don't create model here!
    def create(self, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        # Just return validated data unchanged
        return validated_data


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


class IngestSerializer(serializers.Serializer[Dict[str, Any]]):
    file = serializers.FileField()
