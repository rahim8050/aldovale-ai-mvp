# Create your views here.
# apps/chat/views.py
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework.request import Request


class MessageCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request) -> Response:
        session_id = request.data.get("session")
        message = request.data.get("message")
        if not session_id or not message:
            return Response(
                {"detail": "Session and message required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Call Ollama local LLM API
        ollama_url = "http://localhost:11434"  # Default Ollama local server port, adjust if needed
        model_name = "llama2"  # Replace with your model name in Ollama

        payload = {
            "model": model_name,
            "prompt": message,
        }

        try:
            resp = requests.post(f"{ollama_url}/chat", json=payload, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            reply = data.get("response") or data.get("text") or "No response from LLM"
        except requests.RequestException as e:
            return Response(
                {"detail": f"LLM request failed: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response({"reply": reply})
