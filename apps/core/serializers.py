from rest_framework import serializers
from typing import Any
from .models import Client, Conversation, Session
import uuid
from typing import Dict


class ClientSerializer(serializers.ModelSerializer[Client]):
    class Meta:
        model = Client
        fields = ["id", "name", "webhook_url", "config"]


class SessionCreateSerializer(serializers.Serializer):
    client_id = serializers.UUIDField()

    def create(self, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        client_id = validated_data["client_id"]

        try:
            client = Client.objects.get(id=client_id)
        except Client.DoesNotExist:
            raise serializers.ValidationError("Client does not exist")

        jwt_jti = str(uuid.uuid4())  # generate unique identifier

        session = Session.objects.create(client=client, jwt_jti=jwt_jti)

        # Return dictionary with session info to satisfy DRF's expected return type
        return {"id": session.id, "client": client}


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
