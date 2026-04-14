import pytest
import time


def generate_slug():
    return f"mod-{int(time.time() * 1000)}"


def generate_email():
    return f"user_{int(time.time() * 1000)}@mail.com"


async def get_auth_headers(client):
    email = generate_email()

    await client.post("/auth/register", json={
        "email": email,
        "password": "123456",
        "first_name": "Test",
        "last_name": "User"
    })

    login = await client.post("/auth/login", json={
        "email": email,
        "password": "123456"
    })

    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


# =========================================
# TC-001: Crear módulo
# =========================================
@pytest.mark.asyncio
async def test_create_module(client):
    headers = await get_auth_headers(client)

    response = await client.post("/modules", json={
        "name": "Blog",
        "slug": generate_slug(),
        "description": "Modulo de blog",
        "version": "1.0",
        "is_system": False,
        "is_active": True,
        "icon": "blog-icon",
        "config_schema": {},
        "admin_url": "/admin/blog"
    }, headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Blog"


# =========================================
# TC-002: No permitir slug duplicado
# =========================================
@pytest.mark.asyncio
async def test_create_module_duplicate_slug(client):
    headers = await get_auth_headers(client)
    slug = generate_slug()

    await client.post("/modules", json={
        "name": "Blog",
        "slug": slug,
        "description": "Modulo de blog",
        "version": "1.0",
        "is_system": False,
        "is_active": True,
        "icon": "blog-icon",
        "config_schema": {},
        "admin_url": "/admin/blog"
    }, headers=headers)

    response = await client.post("/modules", json={
        "name": "Otro",
        "slug": slug,
        "description": "Duplicado",
        "version": "1.0",
        "is_system": False,
        "is_active": True,
        "icon": "icon",
        "config_schema": {},
        "admin_url": "/admin"
    }, headers=headers)

    assert response.status_code == 400


# =========================================
# TC-003: Listar módulos
# =========================================
@pytest.mark.asyncio
async def test_list_modules(client):
    headers = await get_auth_headers(client)

    response = await client.get("/modules", headers=headers)

    assert response.status_code == 200
    assert isinstance(response.json(), list)


# =========================================
# TC-004: Obtener módulo por ID
# =========================================
@pytest.mark.asyncio
async def test_get_module(client):
    headers = await get_auth_headers(client)

    create = await client.post("/modules", json={
        "name": "Test",
        "slug": generate_slug(),
        "description": "desc",
        "version": "1.0",
        "is_system": False,
        "is_active": True,
        "icon": "icon",
        "config_schema": {},
        "admin_url": "/admin"
    }, headers=headers)

    module_id = create.json()["id"]

    response = await client.get(f"/modules/{module_id}", headers=headers)

    assert response.status_code == 200
    assert response.json()["id"] == module_id


# =========================================
# TC-005: Obtener módulo inexistente
# =========================================
@pytest.mark.asyncio
async def test_get_module_not_found(client):
    headers = await get_auth_headers(client)

    response = await client.get("/modules/99999", headers=headers)

    assert response.status_code == 404


# =========================================
# TC-006: Actualizar módulo
# =========================================
@pytest.mark.asyncio
async def test_update_module(client):
    headers = await get_auth_headers(client)

    create = await client.post("/modules", json={
        "name": "Old",
        "slug": generate_slug(),
        "description": "desc",
        "version": "1.0",
        "is_system": False,
        "is_active": True,
        "icon": "icon",
        "config_schema": {},
        "admin_url": "/admin"
    }, headers=headers)

    module_id = create.json()["id"]

    response = await client.put(f"/modules/{module_id}", json={
        "name": "Updated"
    }, headers=headers)

    assert response.status_code == 200
    assert response.json()["name"] == "Updated"


# =========================================
# TC-007: Actualizar módulo inexistente
# =========================================
@pytest.mark.asyncio
async def test_update_module_not_found(client):
    headers = await get_auth_headers(client)

    response = await client.put("/modules/99999", json={
        "name": "Fail"
    }, headers=headers)

    assert response.status_code == 404


# =========================================
# TC-008: Eliminar módulo
# =========================================
@pytest.mark.asyncio
async def test_delete_module(client):
    headers = await get_auth_headers(client)

    create = await client.post("/modules", json={
        "name": "Delete",
        "slug": generate_slug(),
        "description": "desc",
        "version": "1.0",
        "is_system": False,
        "is_active": True,
        "icon": "icon",
        "config_schema": {},
        "admin_url": "/admin"
    }, headers=headers)

    module_id = create.json()["id"]

    response = await client.delete(f"/modules/{module_id}", headers=headers)

    assert response.status_code == 204


# =========================================
# TC-009: Eliminar módulo inexistente
# =========================================
@pytest.mark.asyncio
async def test_delete_module_not_found(client):
    headers = await get_auth_headers(client)

    response = await client.delete("/modules/99999", headers=headers)

    assert response.status_code == 404