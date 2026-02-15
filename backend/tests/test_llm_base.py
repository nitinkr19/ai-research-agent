"""Tests for app.llm.base."""

import pytest
from app.llm.base import BaseLLMProvider


class ConcreteProvider(BaseLLMProvider):
    """Concrete implementation for testing abstract base."""

    def generate(self, messages):
        return "ok"

    def __repr__(self):
        return "ConcreteProvider()"


def test_base_provider_can_be_subclassed():
    """BaseLLMProvider can be subclassed and instantiated."""
    p = ConcreteProvider()
    assert p.generate([{"role": "user", "content": "hi"}]) == "ok"
    assert "ConcreteProvider" in repr(p)


def test_base_provider_requires_generate():
    """Subclass without generate raises TypeError on instantiation."""
    class IncompleteProvider(BaseLLMProvider):
        def __repr__(self):
            return "Incomplete()"

    with pytest.raises(TypeError):
        IncompleteProvider()
