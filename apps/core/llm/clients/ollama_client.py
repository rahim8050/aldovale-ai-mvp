from __future__ import annotations

import httpx
from typing import Any, Dict
from django.conf import settings


class OllamaClient:
    """
    Local LLM client for Ollama.
    Works with the same interface as all other providers.
    """

    def __init__(self) -> None:
        self.base_url: str = settings.OLLAMA_BASE_URL
        self.model: str = settings.OLLAMA_MODEL
        self.client = httpx.Client(timeout=30.0)

    def generate(self, prompt: str) -> str:
        payload: Dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }

        response = self.client.post(
            f"{self.base_url}/api/generate",
            json=payload,
        )
        response.raise_for_status()

        data = response.json()
        response_text = data.get("response")
        if response_text is None:
            # Optional: log or raise an exception if no response key
            return ""
        return str(response_text)
