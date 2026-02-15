"""
Ollama provider for local models (llama2, mistral, etc.).
Works with Ollama running at OLLAMA_BASE_URL.
"""

# from typing import List, Dict, Any
import json
import requests

from app.llm.base import BaseLLMProvider
from openai import OpenAI
from app.core.config import settings


class OllamaProvider(BaseLLMProvider):
    """LLM provider for local Ollama models."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama2"):
        self.base_url = base_url.rstrip("/")
        self.model = model

    # async def complete(
    #     self,
    #     messages: List[Dict[str, str]],
    #     **kwargs: Any,
    # ) -> str:
    #     """Call Ollama Chat API."""
    #     async with httpx.AsyncClient(timeout=120.0) as client:
    #         response = await client.post(
    #             f"{self.base_url}/api/chat",
    #             json={"model": self.model, "messages": messages, "stream": False},
    #         )
    #         response.raise_for_status()
    #         data = response.json()
    #         return data.get("message", {}).get("content", "")

    def __repr__(self) -> str:
        return f"OllamaProvider(model={self.model}, url={self.base_url})"

    def generate(self, messages):
        prompt = "\n".join([m["content"] for m in messages])

        response = requests.post(
            f"{settings.ollama_base_url}/api/generate",
            json={
                "model": settings.ollama_model,
                "prompt": prompt,
                "stream": False
            }
        )

        print("STATUS:", response.status_code)
        print("RAW:", response.text)
        return response.json()["response"]
    
    def generate_stream(self, messages):
        prompt = "\n".join([m["content"] for m in messages])

        response = requests.post(
            f"{settings.ollama_base_url}/api/generate",
            json={
                "model": settings.ollama_model,
                "prompt": prompt,
                "stream": True
            },
            stream=True
        )

        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))

                if "response" in data:
                    yield data["response"]
