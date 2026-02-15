"""Tests for app.tools.base."""

import pytest
from app.tools.base import Tool


class ConcreteTool(Tool):
    """Concrete tool for testing abstract base."""

    def run(self, query: str) -> str:
        return f"result: {query}"


def test_tool_base_can_be_subclassed():
    """Tool base can be subclassed and run returns result."""
    t = ConcreteTool()
    assert t.run("hello") == "result: hello"


def test_tool_base_requires_run():
    """Subclass without run cannot be instantiated - run is abstract."""
    class IncompleteTool(Tool):
        pass

    with pytest.raises(TypeError):
        IncompleteTool()
