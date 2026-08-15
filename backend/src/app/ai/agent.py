from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.graph.state import CompiledStateGraph

from app.ai.tools import get_current_time
from app.core.config import get_settings

settings = get_settings()


def build_agent(checkpointer: BaseCheckpointSaver) -> CompiledStateGraph:
    """One example LangGraph agent with one tool, checkpointed to Postgres so conversations
    survive a backend restart. The LLM call goes through `init_chat_model` so swapping
    providers is a one-line config change (settings.llm_model), not a rewrite — see
    design.md's AI-agent decision.

    Uses `langchain.agents.create_agent`, not the older `langgraph.prebuilt.create_react_agent`
    — the latter is deprecated as of LangGraph v1.0 and slated for removal in v2.0."""
    model = init_chat_model(settings.llm_model, api_key=settings.anthropic_api_key)
    return create_agent(model, tools=[get_current_time], checkpointer=checkpointer)
