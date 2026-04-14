import pytest
from httpx import AsyncClient
from packages.modules.blog.models import Post, PostStatus
from packages.core.models.site import Site

@pytest.mark.asyncio
async def test_render_full_site_flow(client: AsyncClient, default_site, db_session):
    """
    TEST 1: Cubre render_site_page, inject_blog_posts y _get_page_content.
    Este test es una 'bomba' de coverage porque atraviesa casi todo el archivo.
    """
    # 1. Creamos un Post para que entre a la lógica de inject_blog_posts
    new_post = Post(
        title="Post de Prueba Coverage",
        slug="post-prueba",
        content="Contenido del post",
        status=PostStatus.PUBLISHED,
        site_id=default_site.id
    )
    db_session.add(new_post)
    
    # 2. Preparamos el HTML con el placeholder que busca tu función
    default_site.settings = {
        "htmlFinal": "<div>Aquí aparecerán tus noticias publicadas automáticamente</div>",
        "cssFinal": "body { color: red; }"
    }
    await db_session.commit()

    # 3. Ejecutamos la ruta principal
    response = await client.get(f"/{default_site.slug}")
    
    assert response.status_code == 200
    assert "Post de Prueba Coverage" in response.text  # Verifica que se inyectó el blog
    assert "body { color: red; }" in response.text      # Verifica que cargó el CSS

@pytest.mark.asyncio
async def test_public_api_info_and_errors(client: AsyncClient, default_site):
    """
    TEST 2: Cubre las rutas de API info y los errores 404.
    """
    # Probar info del sitio
    resp = await client.get(f"/{default_site.slug}/api/info")
    assert resp.status_code == 200
    assert resp.json()["slug"] == default_site.slug

    # Probar error de sitio no encontrado (Cubre el bloque raise HTTPException)
    resp = await client.get("/sitio-que-no-existe/api/info")
    assert resp.status_code == 404

@pytest.mark.asyncio
async def test_subpage_and_blog_detail(client: AsyncClient, default_site, db_session):
    """
    TEST 3: Cubre render_site_subpage_or_blog_post (la ruta más larga).
    """
    # Probar ver el detalle de un post (la parte del HTMLResponse al final del archivo)
    response = await client.get(f"/{default_site.slug}/post-prueba")
    assert response.status_code == 200
    assert "Volver al inicio" in response.text