from typing import Any, Dict
from apps.core.llm.clients.ollama_client import OllamaClient


class DummyResponse:
    def __init__(self, json_data: Dict[str, Any]) -> None:
        self._json = json_data

    def raise_for_status(self) -> None:
        pass  # simulate no HTTP error

    def json(self) -> Dict[str, Any]:
        return self._json


def test_generate_calls_httpx_client_post(mocker: Any, settings: Any) -> None:
    settings.OLLAMA_BASE_URL = "http://localhost:11434"
    settings.OLLAMA_MODEL = "test-model"
    client = OllamaClient()

    mock_post = mocker.patch.object(
        client.client, "post", return_value=DummyResponse({"response": "Hello"})
    )

    response = client.generate("Test prompt")

    mock_post.assert_called_once_with(
        f"{settings.OLLAMA_BASE_URL}/api/generate",
        json={
            "model": settings.OLLAMA_MODEL,
            "prompt": "Test prompt",
            "stream": False,
        },
    )
    assert response == "Hello"


def test_generate_returns_empty_string_if_no_response(
    mocker: Any, settings: Any
) -> None:
    settings.OLLAMA_BASE_URL = "http://localhost:11434"
    settings.OLLAMA_MODEL = "test-model"
    client = OllamaClient()

    mocker.patch.object(client.client, "post", return_value=DummyResponse({}))

    response = client.generate("Another prompt")
    assert response == ""
