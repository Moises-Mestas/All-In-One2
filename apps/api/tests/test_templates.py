import pytest
import time
from packages.core.models.template import Template


def generate_slug():
    return f"template-{int(time.time() * 1000)}"


@pytest.mark.asyncio
async def test_create_template(db_session):
    template = Template(
        name="Test Template",
        slug=generate_slug(),
        description="Test desc",
        is_active=True
    )
    db_session.add(template)
    await db_session.commit()
    await db_session.refresh(template)
    assert template.id is not None