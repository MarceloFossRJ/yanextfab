import json
from collections.abc import AsyncIterator
from typing import Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

from app.models.user import User
from app.users import current_active_user

router = APIRouter(prefix="/ai", tags=["ai"])


class ChatRequest(BaseModel):
    conversation_id: str
    message: str


def _extract_text(content: Any) -> str:
    """Message content is either a plain string or a list of content blocks (Anthropic's
    streaming format); normalize both to plain text for the SSE payload."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(
            block.get("text", "")
            for block in content
            if isinstance(block, dict) and block.get("type") == "text"
        )
    return ""


async def _stream_agent_response(agent: Any, chat: ChatRequest, user: User) -> AsyncIterator[str]:
    # Thread ID scoped per-user so nobody can resume another user's conversation by guessing
    # a conversation_id.
    config = {"configurable": {"thread_id": f"{user.id}:{chat.conversation_id}"}}

    try:
        async for chunk, metadata in agent.astream(
            {"messages": [{"role": "user", "content": chat.message}]},
            config=config,
            stream_mode="messages",
        ):
            if metadata.get("langgraph_node") == "tools":
                continue
            text = _extract_text(getattr(chunk, "content", None))
            if text:
                yield f"data: {json.dumps({'type': 'token', 'content': text})}\n\n"
        yield f"data: {json.dumps({'type': 'done'})}\n\n"
    except Exception as exc:  # noqa: BLE001 — surface as an SSE error event, not a crash
        yield f"data: {json.dumps({'type': 'error', 'message': str(exc)})}\n\n"


@router.post("/chat/stream")
async def chat_stream(
    request: Request, chat: ChatRequest, user: User = Depends(current_active_user)
) -> StreamingResponse:
    agent = request.app.state.agent
    return StreamingResponse(
        _stream_agent_response(agent, chat, user), media_type="text/event-stream"
    )
