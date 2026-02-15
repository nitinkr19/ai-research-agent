"""Tests for app.agent.executor."""

import pytest
from unittest.mock import patch, MagicMock


def test_chunk_text():
    """chunk_text splits text into word-based chunks."""
    from app.agent.executor import chunk_text

    text = " ".join(["word"] * 500)
    chunks = chunk_text(text, chunk_size=100)
    assert len(chunks) >= 4
    assert all(len(c.split()) <= 100 for c in chunks)
    assert " ".join(chunks).replace("  ", " ") == text


@patch("app.agent.executor.search_tool")
@patch("app.agent.executor.create_plan")
@patch("app.agent.executor.llm")
def test_run_agent(mock_llm, mock_plan, mock_search_tool):
    """run_agent returns plan and report."""
    mock_plan.return_value = ["Q1", "Q2"]
    mock_search_tool.run = MagicMock(return_value="result for Q")
    mock_llm.generate.return_value = "Final report here"

    from app.agent.executor import run_agent

    result = run_agent("AI topic")
    assert "plan" in result
    assert "report" in result
    assert result["plan"] == ["Q1", "Q2"]
    assert result["report"] == "Final report here"
