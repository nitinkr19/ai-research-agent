from app.core.config import settings
from app.tools.search import SearchTool
from app.tools.tavily_search import TavilySearchTool


def get_search_tool():

    if settings.search_tool.lower() == "local":
        return SearchTool()

    elif settings.search_tool.lower() == "tavily":
        return TavilySearchTool()

    else:
        raise ValueError("Invalid SEARCH_PROVIDER")
