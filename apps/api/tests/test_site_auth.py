"""
========================================
TEST SUITE: Auth de Sitio - End Users (TC-022)
========================================
Módulo: packages.modules.auth.routes
Funciones testadas:
- register (TC-022: Registro de cliente final en sitio)
"""

import pytest
import time


def generate_slug():
    """Genera un slug único para cada test"""
    return f"site-{int(time.time() * 1000)}"


def generate_email():
    """Genera un email único para cada test"""
    return f"user_{int(time.time() * 1000)}@mail.com"


async def create_site(client):
    """Helper: Crea un sitio de tenant"""
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
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.post("/sites", json={
        "name": "Tienda Cliente",
        "slug": generate_slug(),
        "is_template": False
    }, headers=headers)

    return response.json()["id"]


# =========================================
# TC-022: Registro de cliente final en sitio
# =========================================
@pytest.mark.asyncio
async def test_site_user_register(client):
    """TC-022: Un cliente final puede registrarse en el sitio del tenant"""
    site_id = await create_site(client)

    cliente_email = f"cliente_{int(time.time() * 1000)}@test.com"

    response = await client.post(f"/api/v1/sites/{site_id}/auth/register", json={
        "email": cliente_email,
        "password": "123456",
        "first_name": "Juan",
        "last_name": "Perez",
        "phone": "999888777"
    })

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == cliente_email
    assert data["first_name"] == "Juan"
    assert data["last_name"] == "Perez"
