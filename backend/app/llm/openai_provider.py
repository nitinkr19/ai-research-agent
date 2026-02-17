"""
OpenAI API provider using openai Python package.
Requires OPENAI_API_KEY in .env.
"""

from typing import List, Dict, Any

from app.llm.base import BaseLLMProvider
from openai import OpenAI
from app.core.config import settings


class OpenAIProvider(BaseLLMProvider):
    """LLM provider for OpenAI API (GPT-4, GPT-3.5, etc.)."""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key=settings.openai_api_key)

    def __repr__(self) -> str:
        return f"OpenAIProvider(model={self.model})"
    
    def generate(self, messages):
        response = self.client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            temperature=0.3,
        )
        return response.choices[0].message.content

    def generate_stream(self, messages):

        response = self.client.chat.completions.create(
            model=settings.openai_model,   # e.g. "gpt-4o-mini"
            messages=messages,
            stream=True,
        )

        for chunk in response:
            if chunk.choices:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    yield delta.content
