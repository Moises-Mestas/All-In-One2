import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.pool import StaticPool
from httpx import AsyncClient, ASGITransport

# Importaciones de tu proyecto
from app.main import app
from app.db.database import get_db
from packages.core.models import Base
from packages.core.models.site import Site
from packages.core.models.user import User
from app.core.security import get_password_hash

# Configuración de base de datos en memoria para tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Crea las tablas y limpia la base de datos para cada test"""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    """Configura el cliente HTTP para los tests"""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="https://testserver"  
    ) as c:
        yield c

    app.dependency_overrides.clear()

# ==========================================
# FIXTURES NECESARIAS PARA TUS TESTS
# ==========================================

@pytest_asyncio.fixture(scope="function")
async def default_user(db_session):
    """Crea un usuario dueño del sitio con los campos correctos del modelo"""
    user = User(
        email="test@example.com",
        password_hash=get_password_hash("password123"), # Corregido de hashed_password a password_hash
        first_name="Moisés", # Añadido campo obligatorio
        last_name="Mestas",  # Añadido campo obligatorio
        role="admin"         # Usamos el campo 'role' que sí existe en tu modelo
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user

@pytest_asyncio.fixture(scope="function")
async def default_site(db_session, default_user):
    """Crea el sitio que tus tests necesitan encontrar"""
    site = Site(
        name="Sitio de Prueba",
        slug="test-site",
        domain_name="testserver", 
        owner_id=default_user.id,
        settings={
            "htmlFinal": "<div>Aquí aparecerán tus noticias publicadas automáticamente</div>",
            "cssFinal": "body { margin: 0; }"
        }
    )
    db_session.add(site)
    await db_session.commit()
    await db_session.refresh(site)
    return site