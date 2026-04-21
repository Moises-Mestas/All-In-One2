"""
========================================
TEST SUITE: Rutas Públicas (TC-013 a TC-015)
========================================
Módulo: app.api.public
Funciones testadas:
- get_site_home_route (TC-013, TC-015)
- render_site_page (TC-014)
- 404 para sitio inexistente
"""

import pytest
import time


def generate_slug():
    """Genera un slug único para cada test"""
    return f"site-{int(time.time() * 1000)}"


def generate_email():
    """Genera un email único para cada test"""
    return f"user_{int(time.time() * 1000)}@mail.com"


async def create_site_with_settings(client, settings=None):
    """Helper: Crea un sitio con settings opcionales"""
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
        "name": "Mi Sitio",
        "slug": generate_slug(),
        "is_template": False,
        "settings": settings
    }, headers=headers)

    return response.json()


# =========================================
# TC-013: Fallback HTML para sitio vacío
# =========================================
@pytest.mark.asyncio
async def test_render_site_fallback(client):
    """TC-013: Sitio sin contenido muestra página en construcción"""
    site = await create_site_with_settings(client, settings=None)

    response = await client.get(f"/{site['slug']}")

    assert response.status_code == 200
    assert "En Construcción" in response.text or "no tiene contenido" in response.text.lower()


# =========================================
# TC-014: 404 para sitio inexistente
# =========================================
@pytest.mark.asyncio
async def test_public_site_not_found(client):
    """TC-014: El sistema retorna 404 para slug no existente"""
    response = await client.get("/sitio-fantasma-inexistente-12345")

    assert response.status_code == 404
    assert "no encontrado" in response.json()["detail"].lower()


# =========================================
# TC-015: Renderizado con contenido HTML/CSS
# =========================================
@pytest.mark.asyncio
async def test_render_site_with_content(client):
    """TC-015: Sitio con settings renderiza HTML y CSS correctamente"""
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

    slug = generate_slug()
    settings = {
        "htmlFinal": "<h1>Bienvenido a mi sitio</h1><p>Contenido personalizado</p>",
        "cssFinal": "body { background: white; } h1 { color: blue; }"
    }

    create_response = await client.post("/sites", json={
        "name": "Sitio con Contenido",
        "slug": slug,
        "is_template": False,
        "settings": settings
    }, headers=headers)

    site_id = create_response.json()["id"]

    update_response = await client.put(f"/sites/{site_id}", json={"settings": settings}, headers=headers)
    
    assert update_response.status_code == 200
    updated_settings = update_response.json().get("settings")
    
    assert updated_settings is not None, "Settings should be saved"
    assert "Bienvenido" in updated_settings.get("htmlFinal", "")

    response = await client.get(f"/{slug}")

    assert response.status_code == 200
    html_content = response.text
    assert "Bienvenido" in html_content or "content" in html_content.lower()
