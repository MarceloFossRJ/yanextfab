import uuid
from collections.abc import AsyncGenerator

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.database import get_async_session
from app.core.mail import send_password_reset_email
from app.models.user import User

settings = get_settings()


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    yield SQLAlchemyUserDatabase(session, User)


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = settings.jwt_secret
    verification_token_secret = settings.jwt_secret

    async def on_after_forgot_password(
        self, user: User, token: str, request: Request | None = None
    ) -> None:
        # fastapi-users only calls this after confirming the user exists, and the
        # forgot-password *router* always responds identically either way — see
        # specs/authentication/spec.md's "Recovery Request Confidentiality" requirement.
        await send_password_reset_email(user.email, token)


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
) -> AsyncGenerator[UserManager, None]:
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.jwt_secret, lifetime_seconds=settings.jwt_lifetime_seconds)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)

# --- OAuth / social login (disabled by default) ---
# fastapi-users supports OAuth out of the box, but registering provider apps is
# per-project setup, not boilerplate-level (see design.md). To enable it for a
# specific project:
#   1. uv add "fastapi-users[oauth]"
#   2. Register an OAuth app with your provider and set its client id/secret via env vars
#   3. from httpx_oauth.clients.google import GoogleOAuth2
#      google_oauth_client = GoogleOAuth2(client_id, client_secret)
#      app.include_router(
#          fastapi_users.get_oauth_router(google_oauth_client, auth_backend, settings.jwt_secret),
#          prefix="/auth/google",
#          tags=["auth"],
#      )
