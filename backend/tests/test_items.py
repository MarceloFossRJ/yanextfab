from httpx import AsyncClient

USER_A_EMAIL = "owner-a@example.com"
USER_B_EMAIL = "owner-b@example.com"
PASSWORD = "correcthorsebatterystaple"


async def _register_and_login(client: AsyncClient, email: str) -> str:
    await client.post(
        "/auth/register",
        json={
            "email": email,
            "password": PASSWORD,
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
        },
    )
    login_response = await client.post(
        "/auth/jwt/login", data={"username": email, "password": PASSWORD}
    )
    return login_response.json()["access_token"]


def _auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


async def test_create_and_list_items(client: AsyncClient):
    token = await _register_and_login(client, USER_A_EMAIL)

    create_response = await client.post(
        "/items", json={"title": "First item", "description": "hello"}, headers=_auth_headers(token)
    )
    assert create_response.status_code == 201
    created = create_response.json()
    assert created["title"] == "First item"

    list_response = await client.get("/items", headers=_auth_headers(token))
    assert list_response.status_code == 200
    items = list_response.json()
    assert len(items) == 1
    assert items[0]["id"] == created["id"]


async def test_update_item(client: AsyncClient):
    token = await _register_and_login(client, USER_A_EMAIL)
    create_response = await client.post(
        "/items", json={"title": "Original"}, headers=_auth_headers(token)
    )
    item_id = create_response.json()["id"]

    update_response = await client.patch(
        f"/items/{item_id}", json={"title": "Updated"}, headers=_auth_headers(token)
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated"


async def test_delete_item(client: AsyncClient):
    token = await _register_and_login(client, USER_A_EMAIL)
    create_response = await client.post(
        "/items", json={"title": "To delete"}, headers=_auth_headers(token)
    )
    item_id = create_response.json()["id"]

    delete_response = await client.delete(f"/items/{item_id}", headers=_auth_headers(token))
    assert delete_response.status_code == 204

    get_response = await client.get(f"/items/{item_id}", headers=_auth_headers(token))
    assert get_response.status_code == 404


async def test_items_require_authentication(client: AsyncClient):
    response = await client.get("/items")
    assert response.status_code == 401


async def test_users_cannot_access_other_users_items(client: AsyncClient):
    token_a = await _register_and_login(client, USER_A_EMAIL)
    token_b = await _register_and_login(client, USER_B_EMAIL)

    create_response = await client.post(
        "/items", json={"title": "Owned by A"}, headers=_auth_headers(token_a)
    )
    item_id = create_response.json()["id"]

    get_response = await client.get(f"/items/{item_id}", headers=_auth_headers(token_b))
    assert get_response.status_code == 404

    list_response = await client.get("/items", headers=_auth_headers(token_b))
    assert list_response.json() == []
