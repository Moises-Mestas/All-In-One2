import pytest
import time
from packages.modules.blog.services import create_category, get_post_by_slug
from packages.modules.blog.schemas import CategoryCreate


@pytest.mark.asyncio
async def test_create_category(db_session):
    cat = await create_category(db_session, site_id=1, cat_in=CategoryCreate(
        name="Test Category",
        description="Test desc"
    ))
    assert cat.id is not None
    assert cat.slug == "test-category"


@pytest.mark.asyncio
async def test_get_post_by_slug_notfound(db_session):
    from fastapi import HTTPException
    with pytest.raises(HTTPException) as exc:
        await get_post_by_slug(db_session, site_id=1, slug="notfound")
    assert exc.value.status_code == 404