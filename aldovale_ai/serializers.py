# aldovale_ai/serializers.py

from rest_framework import serializers


class TokenObtainSerializer(serializers.Serializer):  # type: ignore
    api_key = serializers.CharField(
        max_length=255,
        write_only=True,
        help_text="Your API key to obtain JWT token",
        error_messages={"blank": "API key must be provided."},
    )


class ChatMessageSerializer(serializers.Serializer):  # type: ignore
    message = serializers.CharField(
        max_length=2000,
        trim_whitespace=True,
        help_text="Message to send to the chat API",
    )
