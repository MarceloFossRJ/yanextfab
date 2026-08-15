import json
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from app.ai.agent import build_agent
from app.ai.router import router as ai_router
from app.api.items import router as items_router
from app.core.config import get_settings
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.users import auth_backend, fastapi_users

settings = get_settings()


def export_openapi_schema(app: FastAPI, output_path: str | Path) -> Path:
    """Writes the app's OpenAPI schema to `output_path`, creating parent dirs as needed."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(app.openapi(), indent=2))
    return path


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Re-exports openapi.json to the shared volume on every startup, so it stays in sync
    on every `uvicorn --reload` restart without a separate backend-side watcher process.
    Also builds the AI agent once, with a Postgres-backed checkpointer kept open for the
    life of the process, so conversation state survives a restart (see ai-agent spec)."""
    if settings.openapi_export_path:
        export_openapi_schema(app, settings.openapi_export_path)

    async with AsyncPostgresSaver.from_conn_string(settings.psycopg_database_url) as checkpointer:
        await checkpointer.setup()
        app.state.agent = build_agent(checkpointer)
        yield


app = FastAPI(title="Yanextfab API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"])
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate), prefix="/auth", tags=["auth"]
)
app.include_router(fastapi_users.get_reset_password_router(), prefix="/auth", tags=["auth"])
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate), prefix="/users", tags=["users"]
)
app.include_router(ai_router)
app.include_router(items_router)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
