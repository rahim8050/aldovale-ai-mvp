from typing import Any
import pytest
from apps.core.llm.factory import get_llm_client
from apps.core.llm.clients.ollama_client import OllamaClient


def test_get_llm_client_returns_ollama(mocker: Any, settings: Any) -> None:
    settings.LLM_PROVIDER = "ollama"
    client = get_llm_client()
    assert isinstance(client, OllamaClient)


def test_get_llm_client_raises_value_error(settings: Any) -> None:
    settings.LLM_PROVIDER = "unsupported"
    with pytest.raises(ValueError) as exc:
        get_llm_client()
    assert "Unsupported LLM provider" in str(exc.value)
