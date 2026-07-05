import importlib
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient


def fake_orchestrate(msg, history, retriever, sonnet, haiku):
    yield "Well, the thing is..."
    yield " rockets are reusable."


@pytest.fixture
def client():
    with patch("backend.main.Retriever"), \
         patch("backend.main.anthropic_lib.Anthropic"):
        import backend.main as m
        importlib.reload(m)
        with patch("backend.main.orchestrate", side_effect=fake_orchestrate):
            yield TestClient(m.app)


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_chat_200(client):
    resp = client.post("/chat", json={"message": "Hi", "history": []})
    assert resp.status_code == 200


def test_chat_content_type_is_sse(client):
    resp = client.post("/chat", json={"message": "Hi", "history": []})
    assert "text/event-stream" in resp.headers["content-type"]


def test_chat_body_contains_done(client):
    resp = client.post("/chat", json={"message": "Hi", "history": []})
    assert "[DONE]" in resp.text


def test_chat_rejects_empty_message(client):
    resp = client.post("/chat", json={"message": "", "history": []})
    assert resp.status_code == 422


def test_chat_accepts_history(client):
    resp = client.post("/chat", json={
        "message": "What next?",
        "history": [
            {"role": "user", "content": "What about Mars?"},
            {"role": "assistant", "content": "It matters."},
        ]
    })
    assert resp.status_code == 200
