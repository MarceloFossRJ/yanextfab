from langchain.agents import create_agent
from langchain_core.language_models.fake_chat_models import FakeMessagesListChatModel
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from app.ai.tools import get_current_time
from app.core.config import get_settings

settings = get_settings()


class _FakeToolCallingChatModel(FakeMessagesListChatModel):
    """create_agent calls bind_tools() on the model; the base fake models don't implement
    it, so this just returns itself unchanged — fine here since the canned response never
    triggers a tool call anyway."""

    def bind_tools(self, tools, *, tool_choice=None, **kwargs):  # noqa: ANN001, ANN003
        return self


async def test_conversation_resumes_after_simulated_restart():
    """Persistence is the actual risk here, not the LLM call — so this test uses a fake chat
    model (deterministic, no API key/network needed) and verifies state survives a brand new
    AsyncPostgresSaver/connection, which is what a real process restart looks like."""
    config: RunnableConfig = {"configurable": {"thread_id": "test-thread-restart"}}
    fake_model = _FakeToolCallingChatModel(responses=[AIMessage(content="Hello there!")])

    async with AsyncPostgresSaver.from_conn_string(
        settings.psycopg_database_url
    ) as checkpointer_before:
        await checkpointer_before.setup()
        agent_before = create_agent(
            fake_model, tools=[get_current_time], checkpointer=checkpointer_before
        )
        await agent_before.ainvoke({"messages": [{"role": "user", "content": "Hi"}]}, config=config)

    # A brand new saver/connection — simulating the backend process having restarted.
    async with AsyncPostgresSaver.from_conn_string(
        settings.psycopg_database_url
    ) as checkpointer_after:
        agent_after = create_agent(
            fake_model, tools=[get_current_time], checkpointer=checkpointer_after
        )
        state = await agent_after.aget_state(config)

    contents = [getattr(m, "content", None) for m in state.values["messages"]]
    assert "Hi" in contents
    assert "Hello there!" in contents
