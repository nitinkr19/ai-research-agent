"""Tests for app.llm.openai_provider."""

import pytest
from unittest.mock import patch, MagicMock, PropertyMock
from app.llm.openai_provider import OpenAIProvider


def test_openai_provider_repr():
    """OpenAIProvider has correct repr."""
    p = OpenAIProvider(api_key="sk-test", model="gpt-4")
    assert "OpenAIProvider" in repr(p)
    assert "gpt-4" in repr(p)


@patch("app.llm.openai_provider.settings")
@patch("app.llm.openai_provider.OpenAI")
def test_openai_provider_generate(mock_openai_class, mock_settings):
    """OpenAIProvider.generate returns response from API."""
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value.choices = [
        MagicMock(message=MagicMock(content="Hello from GPT"))
    ]
    mock_openai_class.return_value = mock_client
    mock_settings.openai_api_key = "sk-test"
    mock_settings.MODEL_NAME = "gpt-4"

    p = OpenAIProvider(api_key="sk-test", model="gpt-4")
    result = p.generate([{"role": "user", "content": "Hi"}])

    assert result == "Hello from GPT"
    mock_client.chat.completions.create.assert_called_once()
