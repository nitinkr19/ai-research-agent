"""Tests for app.agent.planner."""

import pytest
from unittest.mock import patch


@patch("app.agent.planner.get_llm_provider")
def test_create_plan_returns_list_from_json(mock_get_provider):
    """create_plan returns list of questions from LLM JSON response."""
    mock_llm = mock_get_provider.return_value
    mock_llm.generate.return_value = '{"questions": ["Q1", "Q2", "Q3"]}'

    from app.agent.planner import create_plan

    plan = create_plan("machine learning")
    assert plan == ["Q1", "Q2", "Q3"]
    mock_llm.generate.assert_called_once()


@patch("app.agent.planner.get_llm_provider")
def test_create_plan_fallback_on_invalid_json(mock_get_provider):
    """create_plan falls back to [response] when JSON parse fails."""
    mock_llm = mock_get_provider.return_value
    mock_llm.generate.return_value = "Some raw text without valid JSON"

    from app.agent.planner import create_plan

    plan = create_plan("topic")
    assert plan == ["Some raw text without valid JSON"]
