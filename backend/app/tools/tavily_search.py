import asyncio
import requests
import os
from app.tools.base import BaseSearchTool


class TavilySearchTool(BaseSearchTool):

    async def run(self, query: str) -> str:
        return await asyncio.to_thread(self._search_sync, query)

    def _search_sync(self, query: str) -> str:

        response = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": os.getenv("TAVILY_API_KEY"),
                "query": query,
                "search_depth": "advanced",
                "include_answer": True,
                "max_results": 3
            }
        )

        data = response.json()

        results_text = []

        if "results" in data:
            for result in data["results"]:
                results_text.append(
                    f"Title: {result['title']}\n"
                    f"Content: {result['content']}\n"
                )

        return "\n\n".join(results_text)
