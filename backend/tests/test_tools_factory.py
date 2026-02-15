"""Tests for app.tools.factory."""

import pytest


def test_get_search_tool_local(monkeypatch):
    """Factory returns SearchTool when SEARCH_PROVIDER=local."""
    monkeypatch.setenv("SEARCH_PROVIDER", "local")

    from app.core.config import get_settings
    get_settings.cache_clear()

    from app.tools.factory import get_search_tool
    from app.tools.search import SearchTool

    tool = get_search_tool()
    assert isinstance(tool, SearchTool)

    get_settings.cache_clear()


def test_get_search_tool_tavily(monkeypatch):
    """Factory returns TavilySearchTool when SEARCH_PROVIDER=tavily."""
    monkeypatch.setenv("SEARCH_PROVIDER", "tavily")

    from app.core.config import get_settings
    get_settings.cache_clear()

    from app.tools.factory import get_search_tool
    from app.tools.tavily_search import TavilySearchTool

    tool = get_search_tool()
    assert isinstance(tool, TavilySearchTool)

    get_settings.cache_clear()


def test_get_search_tool_invalid(monkeypatch):
    """Factory raises for invalid SEARCH_PROVIDER."""
    monkeypatch.setenv("SEARCH_PROVIDER", "invalid")

    from app.core.config import get_settings
    get_settings.cache_clear()

    from app.tools.factory import get_search_tool

    with pytest.raises(ValueError, match="Invalid SEARCH_PROVIDER"):
        get_search_tool()

    get_settings.cache_clear()
