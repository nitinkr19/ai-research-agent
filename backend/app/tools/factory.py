import os
from app.tools.search import SearchTool
from app.tools.tavily_search import TavilySearchTool


def get_search_tool():

    provider = os.getenv("SEARCH_PROVIDER", "local")

    if provider == "local":
        return SearchTool()

    elif provider == "tavily":
        return TavilySearchTool()

    else:
        raise ValueError("Invalid SEARCH_PROVIDER")
