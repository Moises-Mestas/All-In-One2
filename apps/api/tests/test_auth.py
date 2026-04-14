"""
========================================
TEST SUITE: Autenticación Core (TC-001 a TC-006)
========================================
Módulo: app.api.auth
Funciones testadas:
- register (TC-001, TC-002)
- login (TC-003, TC-004)
- get_me (TC-005, TC-006)
"""

import pytest
import time


def generate_email():
    """Genera un email único para cada test"""
    return f"test_{int(time.time() * 1000)}@mail.com"


# =========================================
# TC-001: Registro exitoso de usuario
# =========================================
@pytest.mark.asyncio
async def test_register_user(client):
    """TC-001: El tenant puede registrarse exitosamente"""
    response = await client.post("/auth/register", json={
        "email": generate_email(),
        "password": "123456",
        "first_name": "Test",
        "last_name": "User"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["email"] is not None
    assert data["first_name"] == "Test"
    assert "id" in data


# =========================================
# TC-002: Rechazo por email duplicado
# =========================================
@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    """TC-002: El sistema rechaza registro con email ya existente"""
    email = generate_email()

    await client.post("/auth/register", json={
        "email": email,
        "password": "123456",
        "first_name": "Test",
        "last_name": "User"
    })

    response = await client.post("/auth/register", json={
        "email": email,
        "password": "123456",
        "first_name": "Test",
        "last_name": "User"
    })

    assert response.status_code == 400
    assert "ya está registrado" in response.json()["detail"]


# =========================================
# TC-003: Login exitoso
# =========================================
@pytest.mark.asyncio
async def test_login_success(client):
    """TC-003: El usuario puede loguearse con credenciales válidas"""
    email = generate_email()

    await client.post("/auth/register", json={
        "email": email,
        "password": "123456",
        "first_name": "Test",
        "last_name": "User"
    })

    response = await client.post("/auth/login", json={
        "email": email,
        "password": "123456"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


# =========================================
# TC-004: Login con credenciales inválidas
# =========================================
@pytest.mark.asyncio
async def test_login_invalid_credentials(client):
    """TC-004: Login falla con credenciales incorrectas"""
    response = await client.post("/auth/login", json={
        "email": "fake@mail.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 401
    assert "incorrectos" in response.json()["detail"]


# =========================================
# TC-005: GET /me autenticado
# =========================================
@pytest.mark.asyncio
async def test_me_authenticated(client):
    """TC-005: Usuario autenticado puede obtener sus datos"""
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

    response = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert data["first_name"] == "Test"


# =========================================
# TC-006: GET /me sin token
# =========================================
@pytest.mark.asyncio
async def test_me_without_token(client):
    """TC-006: Acceso denegado sin token JWT"""
    response = await client.get("/auth/me")
    assert response.status_code in [401, 403]
