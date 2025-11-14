from django.conf import settings

from apps.core.llm.clients.ollama_client import OllamaClient


def get_llm_client() -> OllamaClient:
    provider = settings.LLM_PROVIDER.lower()

    if provider == "ollama":
        return OllamaClient()

    raise ValueError(f"Unsupported LLM provider: {provider}")
