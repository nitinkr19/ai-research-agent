"""Tests for app.tools.search."""

import pytest
from app.tools.search import SearchTool


@pytest.mark.asyncio
async def test_search_tool_run():
    """SearchTool.run returns simulated results for query."""
    tool = SearchTool()
    result = await tool.run("machine learning")
    assert "Simulated" in result or "machine learning" in result
