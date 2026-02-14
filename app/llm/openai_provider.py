"""
OpenAI API provider using openai Python package.
Requires OPENAI_API_KEY in .env.
"""

from typing import List, Dict, Any

from app.llm.base import BaseLLMProvider


class OpenAIProvider(BaseLLMProvider):
    """LLM provider for OpenAI API (GPT-4, GPT-3.5, etc.)."""

    def __init__(self, api_key: str, model: str = "gpt-4"):
        self.api_key = api_key
        self.model = model

    async def complete(
        self,
        messages: List[Dict[str, str]],
        **kwargs: Any,
    ) -> str:
        """Call OpenAI Chat Completions API."""
        try:
            from openai import AsyncOpenAI
        except ImportError:
            raise ImportError("Install openai: pip install openai")

        client = AsyncOpenAI(api_key=self.api_key)
        response = await client.chat.completions.create(
            model=self.model,
            messages=messages,
            **kwargs,
        )
        return response.choices[0].message.content or ""

    def __repr__(self) -> str:
        return f"OpenAIProvider(model={self.model})"
