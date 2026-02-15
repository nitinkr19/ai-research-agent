"""Tests for app.llm.ollama_provider."""

import pytest
from unittest.mock import patch, MagicMock
from app.llm.ollama_provider import OllamaProvider


def test_ollama_provider_repr():
    """OllamaProvider has correct repr."""
    p = OllamaProvider(base_url="http://localhost:11434", model="llama2")
    assert "OllamaProvider" in repr(p)
    assert "llama2" in repr(p)


@patch("app.llm.ollama_provider.requests.post")
def test_ollama_provider_generate(mock_post):
    """OllamaProvider.generate returns response from API."""
    mock_post.return_value.json.return_value = {"response": "Hello from model"}
    mock_post.return_value.status_code = 200

    p = OllamaProvider(base_url="http://localhost:11434", model="llama2")
    with patch("app.llm.ollama_provider.settings") as mock_settings:
        mock_settings.ollama_base_url = "http://localhost:11434"
        mock_settings.ollama_model = "llama2"
        result = p.generate([{"role": "user", "content": "Hi"}])
        assert result == "Hello from model"
    mock_post.assert_called_once()
