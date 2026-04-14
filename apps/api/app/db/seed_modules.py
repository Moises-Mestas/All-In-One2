import sys
sys.path.insert(0, "/app")
sys.path.insert(0, "/app/packages")

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from packages.core.models.module import Module
from packages.core.models.template import Template

SYSTEM_MODULES = [
    {
        "name": "Auth",
        "slug": "auth",
        "description": "Sistema de autenticación y usuarios del sitio",
        "version": "1.0.0",
        "is_system": True,
        "is_active": True,
        "icon": "shield",
    },
    {
        "name": "Blog Editorial",
        "slug": "blog",
        "description": "Crea y publica artículos con categorías y estados.",
        "version": "1.0.0",
        "is_system": True,
        "is_active": True,
        "icon": "edit",
    },
    {
        "name": "Tienda",
        "slug": "tienda",
        "description": "Módulo de tienda virtual con productos, pedidos y carrito de compras",
        "version": "1.0.0",
        "is_system": True,
        "is_active": True,
        "icon": "shopping-cart",
    },
]


async def seed_system_modules(db: AsyncSession):
    """Inserta los módulos del sistema si no existen"""
    for module_data in SYSTEM_MODULES:
        result = await db.execute(
            select(Module).where(Module.slug == module_data["slug"])
        )
        existing = result.scalar_one_or_none()
        
        if not existing:
            module = Module(**module_data)
            db.add(module)
            print(f"✅ Módulo registrado: {module_data['name']}")
        else:
            print(f"⏭️  Módulo ya existe: {module_data['name']}")
    
    await db.commit()
