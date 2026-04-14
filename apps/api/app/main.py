import sys
import os
sys.path.insert(0, "/app")
sys.path.insert(0, "/app/packages")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# 1. CORE ROUTERS
from app.api import auth_router, sites_router, public_router, modules_router, site_modules_router

# 2. MODULE ROUTERS
from packages.modules.auth.routes import router as site_auth_router
from packages.modules.blog.routes import router as blog_router
from packages.modules.store.routes import router as tienda_router

# 3. DATABASE & SEED
from app.db.database import engine, get_db
from app.db.seed_modules import seed_system_modules

# 4. MODELOS DEL CORE
from packages.core.models import Base
from packages.core.models.user import User
from packages.core.models.site import Site
from packages.core.models.module import Module
from packages.core.models.site_module import SiteModule

# 5. MODELOS DE LOS MÓDULOS
from packages.modules.auth.models import SiteUser, AuthSession, PasswordResetToken
from packages.modules.blog.models import Category, Post 
from packages.modules.store.models import Categoria, Producto, Pedido, ItemPedido, Carrito, ItemCarrito

from fastapi.staticfiles import StaticFiles
from app.api import templates


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # Esto creará las tablas del Blog porque ya las importamos arriba
        await conn.run_sync(Base.metadata.create_all)
    
    async for db in get_db():
        await seed_system_modules(db)
        break
    
    yield

app = FastAPI(title="CMS API", lifespan=lifespan)
os.makedirs("/app/uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="/app/uploads"), name="uploads")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- RUTAS DEL CORE ---
app.include_router(auth_router)
app.include_router(sites_router)
app.include_router(modules_router)
app.include_router(site_modules_router)

# --- RUTAS DE LOS MÓDULOS ---
app.include_router(site_auth_router)
app.include_router(blog_router)
app.include_router(tienda_router)

# 👇 ¡AQUÍ ESTÁ LA CORRECCIÓN MÁGICA! 👇
# El router de plantillas TIENE que ir antes del router público.
app.include_router(templates.router)

# 🚨 EL ROUTER PÚBLICO SIEMPRE AL FINAL 🚨
# (Para que la ruta /{slug} no intercepte las rutas /api/...)
app.include_router(public_router)

@app.get("/")
def read_root():
    return {"message": "CMS API funcionando", "version": "1.0.0"}