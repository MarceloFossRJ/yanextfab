from httpx import AsyncClient
from sqlalchemy import select

TEST_EMAIL = "user@example.com"
TEST_PASSWORD = "correcthorsebatterystaple"


async def _register(client: AsyncClient, email: str = TEST_EMAIL, password: str = TEST_PASSWORD):
    return await client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
        },
    )


async def _login(client: AsyncClient, email: str, password: str):
    return await client.post("/auth/jwt/login", data={"username": email, "password": password})


async def test_register_creates_active_user(client: AsyncClient):
    response = await _register(client)
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == TEST_EMAIL
    assert body["is_active"] is True


async def test_register_duplicate_email_rejected(client: AsyncClient):
    await _register(client)
    response = await _register(client)
    assert response.status_code == 400


async def test_password_is_hashed_not_stored_plaintext(client: AsyncClient):
    await _register(client)

    from app.core.database import async_session_maker
    from app.models.user import User

    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.email == TEST_EMAIL)  # pyright: ignore[reportArgumentType]
        )
        user = result.scalar_one()
        assert user.hashed_password != TEST_PASSWORD


async def test_login_with_correct_credentials_succeeds(client: AsyncClient):
    await _register(client)
    response = await _login(client, TEST_EMAIL, TEST_PASSWORD)
    assert response.status_code == 200
    assert "access_token" in response.json()


async def test_login_with_wrong_password_rejected(client: AsyncClient):
    await _register(client)
    response = await _login(client, TEST_EMAIL, "wrong-password")
    assert response.status_code == 400


async def test_login_with_unregistered_email_rejected(client: AsyncClient):
    response = await _login(client, "nobody@example.com", TEST_PASSWORD)
    assert response.status_code == 400


async def test_users_me_requires_authentication(client: AsyncClient):
    response = await client.get("/users/me")
    assert response.status_code == 401


async def test_users_me_returns_current_user_with_valid_token(client: AsyncClient):
    await _register(client)
    login_response = await _login(client, TEST_EMAIL, TEST_PASSWORD)
    token = login_response.json()["access_token"]

    response = await client.get("/users/me", headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 200
    assert response.json()["email"] == TEST_EMAIL


async def test_forgot_password_sends_email_for_known_user(client: AsyncClient, monkeypatch):
    sent = {}

    async def fake_send(email: str, token: str) -> None:
        sent["email"] = email
        sent["token"] = token

    monkeypatch.setattr("app.users.send_password_reset_email", fake_send)

    await _register(client)
    response = await client.post("/auth/forgot-password", json={"email": TEST_EMAIL})

    assert response.status_code == 202
    assert sent["email"] == TEST_EMAIL
    assert sent["token"]


async def test_forgot_password_confidential_for_unknown_user(client: AsyncClient, monkeypatch):
    called = False

    async def fake_send(email: str, token: str) -> None:
        nonlocal called
        called = True

    monkeypatch.setattr("app.users.send_password_reset_email", fake_send)

    response = await client.post("/auth/forgot-password", json={"email": "nobody@example.com"})

    assert response.status_code == 202
    assert called is False


async def test_reset_password_with_valid_token_changes_password(client: AsyncClient, monkeypatch):
    captured = {}

    async def fake_send(email: str, token: str) -> None:
        captured["token"] = token

    monkeypatch.setattr("app.users.send_password_reset_email", fake_send)

    await _register(client)
    await client.post("/auth/forgot-password", json={"email": TEST_EMAIL})

    new_password = "newcorrecthorsebattery"
    reset_response = await client.post(
        "/auth/reset-password", json={"token": captured["token"], "password": new_password}
    )
    assert reset_response.status_code == 200

    old_login = await _login(client, TEST_EMAIL, TEST_PASSWORD)
    assert old_login.status_code == 400

    new_login = await _login(client, TEST_EMAIL, new_password)
    assert new_login.status_code == 200


async def test_reset_password_with_invalid_token_rejected(client: AsyncClient):
    response = await client.post(
        "/auth/reset-password",
        json={"token": "not-a-real-token", "password": "newcorrecthorsebattery"},
    )
    assert response.status_code == 400
