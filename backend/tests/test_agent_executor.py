"""Tests for app.agent.executor."""

import pytest
from unittest.mock import patch, MagicMock, AsyncMock


def test_chunk_text():
    """chunk_text splits text into word-based chunks."""
    from app.agent.executor import chunk_text

    text = " ".join(["word"] * 500)
    chunks = chunk_text(text, chunk_size=100)
    assert len(chunks) >= 4
    assert all(len(c.split()) <= 100 for c in chunks)
    assert " ".join(chunks).replace("  ", " ") == text


@patch("app.agent.executor.get_search_tool")
@patch("app.agent.executor.create_plan")
@patch("app.agent.executor.get_llm_provider")
def test_run_agent(mock_llm, mock_plan, mock_search):
    """run_agent returns plan and report."""
    mock_plan.return_value = ["Q1", "Q2"]
    mock_search_tool = MagicMock()
    # run_agent calls search_tool.run(question) - SearchTool.run is async
    # Executor might need asyncio - mock run to return a string directly for sync
    mock_search_tool.run = MagicMock(return_value="result for Q")
    mock_search.return_value = mock_search_tool
    mock_llm.return_value.generate.return_value = "Final report here"

    from app.agent.executor import run_agent

    result = run_agent("AI topic")
    assert "plan" in result
    assert "report" in result
    assert result["plan"] == ["Q1", "Q2"]
    assert result["report"] == "Final report here"
