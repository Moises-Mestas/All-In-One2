"""
========================================
TEST SUITE: Gestión de Sitios y Core (TC-007 a TC-012)
========================================
Módulo: app.api.sites
Funciones testadas:
- create_site (TC-007, TC-008, TC-009)
- upload_site_image (TC-010)
- update_site (TC-011)
- Aislamiento multitenant (TC-012)
"""

import pytest
import time


def generate_slug():
    """Genera un slug único para cada test"""
    return f"site-{int(time.time() * 1000)}"


def generate_email():
    """Genera un email único para cada test"""
    return f"user_{int(time.time() * 1000)}@mail.com"


async def get_auth_headers(client):
    """Helper: Crea usuario y retorna headers con token"""
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
# TC-007: Crear sitio con slug único
# =========================================
@pytest.mark.asyncio
async def test_create_site_success(client):
    """TC-007: El tenant puede crear un sitio con slug único"""
    headers = await get_auth_headers(client)

    response = await client.post("/sites", json={
        "name": "Mi Empresa",
        "slug": generate_slug(),
        "is_template": False
    }, headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Mi Empresa"
    assert data["is_template"] is False
    assert "id" in data
    assert data["user_id"] is not None


# =========================================
# TC-008: Clonar sitio desde plantilla
# =========================================
@pytest.mark.asyncio
async def test_create_site_from_template(client):
    """TC-008: El sistema clona el settings de una plantilla"""
    headers = await get_auth_headers(client)

    template_response = await client.post("/sites", json={
        "name": "Plantilla Maestra",
        "slug": generate_slug(),
        "is_template": True,
        "settings": {"htmlFinal": "<h1>Template Content</h1>", "cssFinal": "h1 { color: blue; }"}
    }, headers=headers)
    template_id = template_response.json()["id"]

    cloned_response = await client.post("/sites", json={
        "name": "Sitio Clon",
        "slug": generate_slug(),
        "is_template": False,
        "template_id": template_id
    }, headers=headers)

    assert cloned_response.status_code == 201
    cloned_data = cloned_response.json()
    assert cloned_data["name"] == "Sitio Clon"
    assert cloned_data["settings"] is not None
    assert "Template Content" in cloned_data["settings"]["htmlFinal"]


# =========================================
# TC-009: Rechazo por slug duplicado
# =========================================
@pytest.mark.asyncio
async def test_create_site_duplicate_slug(client):
    """TC-009: El sistema rechaza creación con slug existente"""
    headers = await get_auth_headers(client)
    slug = generate_slug()

    await client.post("/sites", json={
        "name": "Empresa 1",
        "slug": slug,
        "is_template": False
    }, headers=headers)

    response = await client.post("/sites", json={
        "name": "Empresa 2",
        "slug": slug,
        "is_template": False
    }, headers=headers)

    assert response.status_code == 400
    assert "slug ya está en uso" in response.json()["detail"]


# =========================================
# TC-010: Subida de imagen
# =========================================
@pytest.mark.asyncio
async def test_upload_site_image(client):
    """TC-010: El tenant puede subir imagen al sitio"""
    headers = await get_auth_headers(client)

    site_response = await client.post("/sites", json={
        "name": "Sitio con Logo",
        "slug": generate_slug(),
        "is_template": False
    }, headers=headers)
    site_id = site_response.json()["id"]

    files = {"file": ("logo.png", b"fake-image-content", "image/png")}
    response = await client.post(
        f"/sites/{site_id}/upload-image",
        files=files,
        headers=headers
    )

    assert response.status_code == 200
    data = response.json()
    assert "url" in data
    assert data["url"].startswith("/uploads/")
    assert data["url"].endswith(".png")


# =========================================
# TC-011: Guardar configuración JSON
# =========================================
@pytest.mark.asyncio
async def test_update_site_settings(client):
    """TC-011: El tenant puede guardar HTML/CSS del editor"""
    headers = await get_auth_headers(client)

    site_response = await client.post("/sites", json={
        "name": "Sitio Editable",
        "slug": generate_slug(),
        "is_template": False
    }, headers=headers)
    site_id = site_response.json()["id"]

    new_settings = {
        "htmlFinal": "<h1>Nuevo Diseño</h1>",
        "cssFinal": "h1 { color: red; }",
        "components": [{"type": "heading", "tagName": "h1"}]
    }

    update_response = await client.put(
        f"/sites/{site_id}",
        json={"settings": new_settings},
        headers=headers
    )

    assert update_response.status_code == 200
    updated_data = update_response.json()
    assert updated_data["settings"]["htmlFinal"] == "<h1>Nuevo Diseño</h1>"


# =========================================
# TC-012: Aislamiento de datos (Multitenancy)
# =========================================
@pytest.mark.asyncio
async def test_cross_tenant_isolation(client):
    """TC-012: Un tenant NO puede modificar sitios de otro"""
    headers_tenant_a = await get_auth_headers(client)
    headers_tenant_b = await get_auth_headers(client)

    site_response = await client.post("/sites", json={
        "name": "Sitio de Tenant A",
        "slug": generate_slug(),
        "is_template": False
    }, headers=headers_tenant_a)
    site_id = site_response.json()["id"]

    response = await client.put(
        f"/sites/{site_id}",
        json={"name": "Intento de Modificación"},
        headers=headers_tenant_b
    )

    assert response.status_code == 404
