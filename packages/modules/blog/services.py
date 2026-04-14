import re
import unicodedata
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from fastapi import HTTPException
from datetime import datetime, timezone

# 👇 CORRECCIÓN 1: Importamos explícitamente la clase PostStatus
from packages.modules.blog.models import Post, Category, PostStatus
from packages.modules.blog.schemas import PostCreate, CategoryCreate, PostUpdate

# 🧠 UTILIDAD: Generador automático de Slugs
def generate_slug(text: str) -> str:
    # 1. Quitar tildes y caracteres especiales (ej: á -> a)
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    # 2. Convertir a minúsculas y reemplazar todo lo que no sea letra o número por guiones
    slug = re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')
    return slug

async def generate_unique_post_slug(db: AsyncSession, site_id: int, title: str) -> str:
    base_slug = generate_slug(title)
    slug = base_slug
    counter = 1
    
    # Bucle para asegurar que el slug no exista en este sitio web
    while True:
        result = await db.execute(select(Post).where(Post.site_id == site_id, Post.slug == slug))
        if not result.scalar_one_or_none():
            return slug
        # Si ya existe, le agregamos un número al final: "mi-post-1", "mi-post-2"
        slug = f"{base_slug}-{counter}"
        counter += 1

# --- SERVICIOS DE POSTS ---

async def create_post(db: AsyncSession, site_id: int, post_in: PostCreate) -> Post:
    # Generamos el slug automáticamente desde el título
    unique_slug = await generate_unique_post_slug(db, site_id, post_in.title)
    
    new_post = Post(
        site_id=site_id,
        slug=unique_slug,
        **post_in.model_dump()
    )
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post

async def get_posts_by_site(db: AsyncSession, site_id: int, only_published: bool = False):
    query = select(Post).where(Post.site_id == site_id)
    
    if only_published:
        # En la web pública, mostramos publicados + los programados cuya hora ya llegó
        now = datetime.now(timezone.utc)
        
        # 👇 CORRECCIÓN 2: Usar PostStatus nativo y validar que haya fecha
        query = query.where(
            or_(
                Post.status == PostStatus.PUBLISHED,
                and_(
                    Post.status == PostStatus.SCHEDULED,
                    Post.published_at.isnot(None), # Asegura que no rompa si es nulo
                    Post.published_at <= now
                )
            )
        )
        
    result = await db.execute(query.order_by(Post.created_at.desc()))
    return result.scalars().all()

async def get_post_by_slug(db: AsyncSession, site_id: int, slug: str) -> Post:
    result = await db.execute(select(Post).where(Post.site_id == site_id, Post.slug == slug))
    post = result.scalar_one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    return post

# --- SERVICIOS DE CATEGORÍAS (Básico) ---

async def create_category(db: AsyncSession, site_id: int, cat_in: CategoryCreate) -> Category:
    slug = generate_slug(cat_in.name) 
    
    new_cat = Category(
        site_id=site_id,
        slug=slug,
        **cat_in.model_dump()
    )
    db.add(new_cat)
    await db.commit()
    await db.refresh(new_cat)
    return new_cat