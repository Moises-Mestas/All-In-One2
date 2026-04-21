import pytest
import time
from packages.modules.blog.services import generate_slug, generate_unique_post_slug, create_post, get_posts_by_site, get_post_by_slug, create_category
from packages.modules.blog.schemas import PostCreate, CategoryCreate
from packages.modules.blog.models import PostStatus


def generate_email():
    return f"test_{int(time.time() * 1000)}@mail.com"


@pytest.mark.asyncio
async def test_generate_slug():
    slug = generate_slug("Hola Mundo")
    assert slug == "hola-mundo"
    
    slug2 = generate_slug("Test de slug!")
    assert slug2 == "test-de-slug"


@pytest.mark.asyncio
async def test_generate_unique_post_slug(db_session):
    slug = await generate_unique_post_slug(db_session, site_id=1, title="Mi Post")
    assert slug == "mi-post"
    
    await create_post(db_session, site_id=1, post_in=PostCreate(
        title="Mi Post", content="Content", status=PostStatus.DRAFT
    ))
    
    slug2 = await generate_unique_post_slug(db_session, site_id=1, title="Mi Post")
    assert slug2 == "mi-post-1"


@pytest.mark.asyncio
async def test_create_post(db_session):
    post = await create_post(db_session, site_id=1, post_in=PostCreate(
        title="Nuevo Post",
        content="Contenido de prueba",
        status=PostStatus.PUBLISHED,
        excerpt="Resumen"
    ))
    
    assert post.id is not None
    assert post.title == "Nuevo Post"
    assert post.slug == "nuevo-post"


@pytest.mark.asyncio
async def test_create_post_duplicate_title(db_session):
    await create_post(db_session, site_id=1, post_in=PostCreate(
        title="Post Duplicado",
        content="Content",
        status=PostStatus.PUBLISHED
    ))
    
    post2 = await create_post(db_session, site_id=1, post_in=PostCreate(
        title="Post Duplicado",
        content="Content",
        status=PostStatus.PUBLISHED
    ))
    
    assert post2.slug == "post-duplicado-1"


@pytest.mark.asyncio
async def test_get_posts_by_site(db_session):
    await create_post(db_session, site_id=1, post_in=PostCreate(
        title="Post 1", content="Content", status=PostStatus.DRAFT
    ))
    await create_post(db_session, site_id=1, post_in=PostCreate(
        title="Post 2", content="Content", status=PostStatus.PUBLISHED
    ))
    await create_post(db_session, site_id=2, post_in=PostCreate(
        title="Post 3", content="Content", status=PostStatus.PUBLISHED
    ))
    
    posts_site1 = await get_posts_by_site(db_session, site_id=1, only_published=False)
    assert len(posts_site1) >= 2
    
    posts_published = await get_posts_by_site(db_session, site_id=1, only_published=True)
    assert all(p.status == PostStatus.PUBLISHED for p in posts_published)


@pytest.mark.asyncio
async def test_get_post_by_slug(db_session):
    post = await create_post(db_session, site_id=1, post_in=PostCreate(
        title="Post Busqueda",
        content="Content",
        status=PostStatus.PUBLISHED
    ))
    
    found = await get_post_by_slug(db_session, site_id=1, slug=post.slug)
    assert found.id == post.id


@pytest.mark.asyncio
async def test_get_post_by_slug_not_found(db_session):
    from fastapi import HTTPException
    
    with pytest.raises(HTTPException) as exc_info:
        await get_post_by_slug(db_session, site_id=1, slug="no-existe")
    
    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_create_category(db_session):
    cat = await create_category(db_session, site_id=1, cat_in=CategoryCreate(
        name="Tecnología",
        description="Posts de tech"
    ))
    
    assert cat.id is not None
    assert cat.slug == "tecnologia"