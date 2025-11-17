from typing import Dict, Any, Optional

import httpx
from django.conf import settings


class OllamaClient:
    def __init__(
        self, base_url: Optional[str] = None, model: Optional[str] = None
    ) -> None:
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self.model = model or settings.OLLAMA_MODEL
        self.client = httpx.Client(timeout=30.0)

    def generate(self, prompt: str) -> str:
        payload: Dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
        }
        response = self.client.post(f"{self.base_url}/api/generate", json=payload)
        response.raise_for_status()
        data = response.json()

        response_str = data.get("response", "")
        if not isinstance(response_str, str):
            return ""

        return response_str
