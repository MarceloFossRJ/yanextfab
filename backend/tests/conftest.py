import os
import re
from collections.abc import AsyncIterator
from urllib.parse import urlsplit, urlunsplit

import asyncpg
import pytest_asyncio
from httpx import ASGITransport, AsyncClient


def _test_database_url() -> str:
    explicit = os.environ.get("TEST_DATABASE_URL")
    if explicit:
        return explicit
    base = os.environ.get(
        "DATABASE_URL", "postgresql+asyncpg://yanextfab:yanextfab@localhost:5432/yanextfab"
    )
    return re.sub(r"/([^/]+)$", r"/\1_test", base)


# Set before importing any app module, since get_settings() is cached at first import.
TEST_DATABASE_URL = _test_database_url()
os.environ["DATABASE_URL"] = TEST_DATABASE_URL

from app.core.database import engine  # noqa: E402
from app.models import item as _item  # noqa: E402,F401
from app.models import user as _user  # noqa: E402,F401
from app.models.base import Base  # noqa: E402


async def _ensure_test_database_exists(url: str) -> None:
    """Self-provisions a dedicated test database on whatever Postgres server DATABASE_URL
    points at (dev docker-compose or a CI service container), so `uv run pytest` never has
    to run against — and can't accidentally wipe — real data."""
    parsed = urlsplit(url.replace("postgresql+asyncpg", "postgresql"))
    db_name = parsed.path.lstrip("/")
    admin_url = urlunsplit(parsed._replace(path="/postgres"))
    conn = await asyncpg.connect(admin_url)
    try:
        exists = await conn.fetchval("SELECT 1 FROM pg_database WHERE datname = $1", db_name)
        if not exists:
            await conn.execute(f'CREATE DATABASE "{db_name}"')
    finally:
        await conn.close()


@pytest_asyncio.fixture(scope="session", autouse=True)
async def _test_database() -> None:
    await _ensure_test_database_exists(TEST_DATABASE_URL)


@pytest_asyncio.fixture(autouse=True)
async def _reset_schema() -> AsyncIterator[None]:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def client() -> AsyncIterator[AsyncClient]:
    from app.main import app

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
