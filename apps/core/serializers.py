from rest_framework import serializers
from .models import Client, Conversation


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name", "webhook_url", "config"]


class SessionCreateSerializer(serializers.Serializer):
    client_id = serializers.UUIDField()


class ConversationSerializer(serializers.ModelSerializer):
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


class IngestSerializer(serializers.Serializer):
    file = serializers.FileField()
