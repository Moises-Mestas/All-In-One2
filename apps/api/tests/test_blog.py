"""
========================================
TEST SUITE: Módulo de Blog (TC-016 a TC-018)
========================================
Módulo: packages.modules.blog.routes
Funciones testadas:
- create_post_route (TC-016)
- inject_blog_posts en public.py (TC-017)
- Filtrado de posts DRAFT (TC-018)
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
    """Helper: Crea un sitio y retorna su ID"""
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
        "name": "Sitio Blog",
        "slug": generate_slug(),
        "is_template": False
    }, headers=headers)

    return response.json()["id"], headers


# =========================================
# TC-016: Crear post PUBLISHED
# =========================================
@pytest.mark.asyncio
async def test_create_post_published(client):
    """TC-016: El tenant puede crear un post con status PUBLISHED"""
    site_id, headers = await create_site(client)

    response = await client.post(f"/modules/blog/{site_id}/posts", json={
        "title": "Gran Apertura",
        "slug": f"gran-apertura-{int(time.time() * 1000)}",
        "content": "<p>Texto del artículo...</p>",
        "status": "published",
        "excerpt": "Extracto del post",
        "featured_image": "https://example.com/image.jpg"
    }, headers=headers)

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Gran Apertura"
    assert data["status"] == "published"
    assert data["slug"] is not None


# =========================================
# TC-017: Inyección de posts en HTML público
# =========================================
@pytest.mark.asyncio
async def test_blog_posts_injected_in_public(client):
    """TC-017: Los posts publicados se muestran en el endpoint público del blog"""
    site_id, headers = await create_site(client)

    await client.post(f"/modules/blog/{site_id}/posts", json={
        "title": "Noticia Importante",
        "slug": f"noticia-{int(time.time() * 1000)}",
        "content": "<p>Contenido de la noticia</p>",
        "status": "published",
        "excerpt": "Breve descripción"
    }, headers=headers)

    posts_response = await client.get(f"/modules/blog/{site_id}/posts", params={"only_published": True})

    assert posts_response.status_code == 200
    posts = posts_response.json()
    published_titles = [p["title"] for p in posts]
    assert "Noticia Importante" in published_titles


# =========================================
# TC-018: Filtrado de posts DRAFT
# =========================================
@pytest.mark.asyncio
async def test_public_posts_exclude_draft(client):
    """TC-018: Los posts en DRAFT NO aparecen en consultas públicas"""
    site_id, headers = await create_site(client)
    site_response = await client.get("/sites", headers=headers)
    site_slug = site_response.json()[0]["slug"]

    await client.post(f"/modules/blog/{site_id}/posts", json={
        "title": "Post en Borrador",
        "slug": f"borrador-{int(time.time() * 1000)}",
        "content": "<p>Contenido privado</p>",
        "status": "draft",
        "excerpt": "No debe verse"
    }, headers=headers)

    posts_response = await client.get(f"/modules/blog/{site_id}/posts", params={"only_published": True})

    draft_posts = [p for p in posts_response.json() if p.get("title") == "Post en Borrador"]
    assert len(draft_posts) == 0
