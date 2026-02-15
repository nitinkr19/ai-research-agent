"""Tests for FastAPI main app."""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Create test client. LLM/provider loaded at import - may fail without env."""
    try:
        from app.main import app
        return TestClient(app)
    except Exception as e:
        pytest.skip(f"Cannot load app (check .env): {e}")


def test_health(client):
    """Health endpoint returns ok."""
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_test_stream(client):
    """Test stream returns SSE chunks."""
    r = client.get("/test-stream")
    assert r.status_code == 200
    assert "text/event-stream" in r.headers.get("content-type", "")
    text = r.text
    assert "Hello 0" in text
    assert "Hello 4" in text
