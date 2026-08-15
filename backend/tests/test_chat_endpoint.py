from httpx import AsyncClient
from langchain_core.messages import AIMessage
from langgraph.checkpoint.memory import InMemorySaver

from app.ai.agent import build_agent
from tests.test_ai_agent import _FakeToolCallingChatModel

TEST_EMAIL = "chatuser@example.com"
TEST_PASSWORD = "correcthorsebatterystaple"


async def test_chat_stream_requires_authentication(client: AsyncClient):
    response = await client.post("/ai/chat/stream", json={"conversation_id": "c1", "message": "hi"})
    assert response.status_code == 401


async def test_chat_stream_returns_token_and_done_events(client: AsyncClient, monkeypatch):
    from app.main import app

    fake_model = _FakeToolCallingChatModel(responses=[AIMessage(content="Hello there!")])
    monkeypatch.setattr("app.ai.agent.init_chat_model", lambda *args, **kwargs: fake_model)

    # A lightweight in-memory checkpointer here — this test exercises the HTTP/SSE wiring,
    # not persistence (that's covered separately in test_ai_agent.py against real Postgres).
    app.state.agent = build_agent(InMemorySaver())
    try:
        await client.post(
            "/auth/register",
            json={
                "email": TEST_EMAIL,
                "password": TEST_PASSWORD,
                "is_active": True,
                "is_superuser": False,
                "is_verified": False,
            },
        )
        login_response = await client.post(
            "/auth/jwt/login", data={"username": TEST_EMAIL, "password": TEST_PASSWORD}
        )
        token = login_response.json()["access_token"]

        async with client.stream(
            "POST",
            "/ai/chat/stream",
            json={"conversation_id": "c1", "message": "hi"},
            headers={"Authorization": f"Bearer {token}"},
        ) as response:
            assert response.status_code == 200
            body = "".join([chunk async for chunk in response.aiter_text()])
    finally:
        del app.state.agent

    assert '"type": "token"' in body
    assert '"type": "done"' in body
