"""Tests for app.agent.prompts."""

from app.agent.prompts import (
    PLANNING_SYSTEM,
    PLANNING_USER,
    EXECUTION_SYSTEM,
    EXECUTION_USER,
)


def test_planning_system_prompt():
    """Planning system prompt is non-empty and mentions plan."""
    assert len(PLANNING_SYSTEM) > 0
    assert "plan" in PLANNING_SYSTEM.lower() or "research" in PLANNING_SYSTEM.lower()


def test_planning_user_has_placeholder():
    """Planning user prompt has {task} placeholder."""
    assert "{task}" in PLANNING_USER
    formatted = PLANNING_USER.format(task="test topic")
    assert "test topic" in formatted


def test_execution_system_prompt():
    """Execution system prompt is non-empty."""
    assert len(EXECUTION_SYSTEM) > 0


def test_execution_user_has_placeholders():
    """Execution user prompt has {task} and {plan} placeholders."""
    assert "{task}" in EXECUTION_USER
    assert "{plan}" in EXECUTION_USER
    formatted = EXECUTION_USER.format(task="topic", plan="1. Step one")
    assert "topic" in formatted
    assert "1. Step one" in formatted
