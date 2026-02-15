"""Tests for app.tools.tavily_search."""

import pytest
from unittest.mock import patch, MagicMock
from app.tools.tavily_search import TavilySearchTool


@patch("app.tools.tavily_search.requests.post")
@pytest.mark.asyncio
async def test_tavily_search_returns_results(mock_post):
    """TavilySearchTool.run returns formatted results from API."""
    mock_post.return_value.json.return_value = {
        "results": [
            {"title": "Article 1", "content": "Content 1"},
            {"title": "Article 2", "content": "Content 2"},
        ]
    }
    mock_post.return_value.status_code = 200

    with patch.dict("os.environ", {"TAVILY_API_KEY": "test-key"}):
        tool = TavilySearchTool()
        result = await tool.run("AI research")

    assert "Article 1" in result
    assert "Content 1" in result
    assert "Article 2" in result
    mock_post.assert_called_once()


@patch("app.tools.tavily_search.requests.post")
@pytest.mark.asyncio
async def test_tavily_search_handles_empty_results(mock_post):
    """TavilySearchTool handles empty results."""
    mock_post.return_value.json.return_value = {}
    mock_post.return_value.status_code = 200

    with patch.dict("os.environ", {"TAVILY_API_KEY": "test-key"}):
        tool = TavilySearchTool()
        result = await tool.run("query")

    assert result == ""
