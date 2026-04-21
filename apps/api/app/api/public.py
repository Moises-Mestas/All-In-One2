import sys
import os
import json
import re
from datetime import datetime, timezone
from typing import Annotated

sys.path.insert(0, "/app")
sys.path.insert(0, "/app/packages")

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from app.db.database import get_db
from packages.core.models.site import Site
from packages.core.models.site_module import SiteModule
from packages.core.models.module import Module
from packages.shared.site_scripts import get_site_scripts
from packages.modules.blog.models import Post, PostStatus

router = APIRouter(tags=["public"])

ERROR_SITIO_NO_ENCONTRADO = "Sitio no encontrado"

def extract_subdomain(host: str) -> str | None:
    if not host: return None
    parts = host.split(".")
    if len(parts) >= 2:
        if parts[-1] in ["localtest", "me"] and len(parts) >= 3: return parts[0]
        if parts[-2:] == ["127", "0", "0", "1"]: return parts[0]
        if "nip" in host and ".nip.io" in host: return parts[0]
    if len(parts) >= 2: return parts[0]
    return None

async def get_site_auth_config(db: AsyncSession, site_id: int) -> dict | None:
    """Obtiene la configuración de auth del sitio si el módulo está activo"""
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        result = await db.execute(
            select(SiteModule, Module).join(Module).where(
                and_(
                    SiteModule.site_id == site_id,
                    Module.slug == "auth",
                    SiteModule.is_active == True
                )
            )
        )
        row = result.first()
        
        if row:
            site_module = row[0]
            logger.info(f"Auth config encontrada para site {site_id}")
            config = site_module.config
            if isinstance(config, str):
                config = json.loads(config)
            return config
        else:
            logger.warning(f"No se encontró site_module activo para auth en site {site_id}")
    except Exception as e:
        logger.error(f"Error obteniendo auth config: {e}")
    
    return None

async def inject_blog_posts(html_content: str, site_id: int, db: AsyncSession) -> str:
    """Inyección quirúrgica: Vence la limpieza de atributos de GrapesJS"""
    
    textos_placeholder = [
        "Aquí aparecerán tus noticias publicadas automáticamente",
        "Los artículos aparecerán aquí automáticamente"
    ]
    
    texto_encontrado = None
    for t in textos_placeholder:
        if t in html_content:
            texto_encontrado = t
            break
            
    if not texto_encontrado:
        return html_content

    try:
        now = datetime.now(timezone.utc)
        result = await db.execute(
            select(Post).where(
                Post.site_id == site_id, 
                or_(
                    Post.status == PostStatus.PUBLISHED,
                    and_(
                        Post.status == PostStatus.SCHEDULED,
                        Post.published_at.isnot(None),
                        Post.published_at <= now
                    )
                )
            ).order_by(Post.created_at.desc())
        )
        posts = result.scalars().all()

        blog_html = ""
        for post in posts:
            img_tag = f'<img src="{post.featured_image}" style="width:100%; height:180px; object-fit:cover; border-radius:4px; margin-bottom: 10px;">' if post.featured_image else ""
            blog_html += f"""
            <div class="blog-card" style="border: 1px solid #eee; padding: 15px; border-radius: 8px; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                {img_tag}
                <h3 style="margin: 10px 0 5px 0; color: #333;">{post.title}</h3>
                <p style="color: #666; font-size: 14px; margin-bottom: 15px;">{post.excerpt or ""}</p>
                <a href="/{post.slug}" style="color: #3498db; font-weight: bold; text-decoration: none; font-size: 14px;">Leer más →</a>
            </div>
            """
            
        if not posts:
            blog_html = '<p style="grid-column: 1 / -1; text-align: center; color: #888;">No hay artículos publicados aún.</p>'

        pos_texto = html_content.find(texto_encontrado)
        if pos_texto != -1:
            inicio_div_gris = html_content.rfind('<div', 0, pos_texto)
            fin_div_gris = html_content.find('</div>', pos_texto) + 6
            
            if inicio_div_gris != -1 and fin_div_gris != -1:
                html_content = html_content[:inicio_div_gris] + blog_html + html_content[fin_div_gris:]

    except Exception as e:
        print(f"Error inyectando Blog: {e}")
        
    return html_content

# ==========================================
# FUNCIONES AUXILIARES PARA REDUCIR COMPLEJIDAD (AÑADIDAS)
# ==========================================
def _get_page_content(settings_data: dict, page_name: str) -> tuple[str, str]:
    multi_pages = settings_data.get("multiPages", [])

    if multi_pages:
        target_name = page_name.lower() if page_name else "inicio"
        page_found = next((p for p in multi_pages if p.get("name") == target_name), None)
        if page_found:
            return page_found.get("html", ""), page_found.get("css", "")
        else:
            raise HTTPException(status_code=404, detail=f"La página '{target_name}' no existe en este sitio.")
    else:
        if page_name: 
            raise HTTPException(status_code=404, detail="Este sitio no tiene subpáginas.")
        return settings_data.get("htmlFinal", ""), settings_data.get("cssFinal", "")

def _get_fallback_html(site_name: str) -> HTMLResponse:
    content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{site_name} - En Construcción</title>
        <style>
            body {{ font-family: system-ui, sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; background: #f5f5f5; }}
            .container {{ text-align: center; padding: 2rem; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>{site_name}</h1>
            <p>Esta página aún no tiene contenido. Usa el editor para crear tu diseño.</p>
        </div>
    </body>
    </html>
    """
    response = HTMLResponse(content=content, status_code=200)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response

# ==========================================
# 2. MOTOR DE RENDERIZADO PRINCIPAL
# ==========================================
async def render_site_page(slug: str, page_name: str, debug: bool, db: AsyncSession):
    """Esta es la función madre que arma tu página con GrapesJS, Auth y Blog"""
    result = await db.execute(select(Site).where(Site.slug == slug))
    site = result.scalar_one_or_none()
    
    if not site: raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    if debug: return JSONResponse(content=site.settings)
        
    settings_data = site.settings or {}
    if isinstance(settings_data, str):
        try: 
            settings_data = json.loads(settings_data)
        # 👇 CORRECCIÓN DE SEGURIDAD: Evita el "bare except" indicando qué error atrapar
        except json.JSONDecodeError: 
            settings_data = {}

    html_final, css_final = _get_page_content(settings_data, page_name)
    
    if not html_final:
        return _get_fallback_html(site.name)
    
    html_final = await inject_blog_posts(html_final, site.id, db)
    
    auth_config = await get_site_auth_config(db, site.id)
    
    site_scripts = get_site_scripts(
        site_id=site.id,
        site_slug=slug,
        html_content=html_final,
        auth_config=auth_config
    )
    
    pagina_armada = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <base href="/{slug}/">
        <title>{site.name}</title>
        <style>body {{ margin: 0; padding: 0; overflow-x: hidden; }} {css_final}</style>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    </head>
    <body>
        {html_final}
        {site_scripts}
    </body>
    </html>
    """
    
    response = HTMLResponse(content=pagina_armada, status_code=200)
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    return response

# 👇 CORRECCIÓN DOCUMENTACIÓN: Documentar el HTTPException 404 en 'responses'
@router.get("/{slug}/api/info", responses={404: {"description": ERROR_SITIO_NO_ENCONTRADO}})
async def get_site_info(slug: str, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Site).where(Site.slug == slug))
    site = result.scalar_one_or_none()
    if not site: raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    return {"id": site.id, "name": site.name, "slug": site.slug}

# 👇 CORRECCIÓN DOCUMENTACIÓN: Documentar el HTTPException 404 en 'responses'
@router.post("/{slug}/api/activate-auth", responses={404: {"description": ERROR_SITIO_NO_ENCONTRADO}})
async def activate_auth_module(slug: str, db: Annotated[AsyncSession, Depends(get_db)]):
    result = await db.execute(select(Site).where(Site.slug == slug))
    site = result.scalar_one_or_none()
    if not site: raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    
    result = await db.execute(select(Module).where(Module.slug == "auth"))
    module = result.scalar_one_or_none()
    if not module: return {"error": "Módulo auth no encontrado"}
    
    result = await db.execute(
        select(SiteModule).where(SiteModule.site_id == site.id, SiteModule.module_id == module.id)
    )
    existing = result.scalar_one_or_none()
    
    if existing:
        existing.is_active = True
        existing.config = {
            "registration_fields": ["email", "password", "first_name", "last_name", "phone"],
            "custom_fields": [],
            "require_verification": False
        }
        await db.commit()
        return {"message": "Módulo auth activado", "config": existing.config}
    else:
        new_sm = SiteModule(
            site_id=site.id,
            module_id=module.id,
            is_active=True,
            config={
                "registration_fields": ["email", "password", "first_name", "last_name", "phone"],
                "custom_fields": [],
                "require_verification": False
            }
        )
        db.add(new_sm)
        await db.commit()
        await db.refresh(new_sm)
        return {"message": "Módulo auth creado y activado", "config": new_sm.config}

# 👇 CORRECCIÓN DOCUMENTACIÓN: Documentar el HTTPException 404 en 'responses'
@router.get("/{site_slug}", responses={404: {"description": ERROR_SITIO_NO_ENCONTRADO}})
async def get_site_home_route(
    site_slug: str, 
    db: Annotated[AsyncSession, Depends(get_db)], 
    debug: bool = False
):
    return await render_site_page(site_slug, "", debug, db)

# 👇 CORRECCIÓN DOCUMENTACIÓN: Documentar el HTTPException 404 en 'responses'
@router.get("/{site_slug}/{post_slug_or_page_name}", responses={404: {"description": ERROR_SITIO_NO_ENCONTRADO}})
async def render_site_subpage_or_blog_post(
    site_slug: str, 
    post_slug_or_page_name: str, 
    db: Annotated[AsyncSession, Depends(get_db)], 
    debug: bool = False
):
    result = await db.execute(select(Site).where(Site.slug == site_slug))
    site = result.scalar_one_or_none()
    if not site: raise HTTPException(404, detail=ERROR_SITIO_NO_ENCONTRADO)

    now = datetime.now(timezone.utc)
    result = await db.execute(
        select(Post).where(
            Post.site_id == site.id, 
            Post.slug == post_slug_or_page_name,
            or_(
                Post.status == PostStatus.PUBLISHED,
                and_(
                    Post.status == PostStatus.SCHEDULED,
                    Post.published_at.isnot(None),
                    Post.published_at <= now
                )
            )
        )
    )
    post = result.scalar_one_or_none()
    
    if not post:
        return await render_site_page(site_slug, post_slug_or_page_name, debug, db)

    return HTMLResponse(content=f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{post.meta_title or post.title}</title>
            <meta name="description" content="{post.meta_description or ''}">
            <style>
                body {{ font-family: system-ui, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 40px 20px; color: #333; }}
                img {{ max-width: 100%; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin: 20px 0; }}
                h1 {{ font-size: 2.5em; color: #1e293b; margin-bottom: 10px; }}
                a.btn-volver {{ display: inline-block; padding: 10px 20px; background: #f1f5f9; color: #475569; text-decoration: none; border-radius: 6px; font-weight: bold; margin-bottom: 30px; transition: background 0.3s; }}
                a.btn-volver:hover {{ background: #e2e8f0; }}
                .post-content {{ font-size: 1.1em; line-height: 1.8; }}
            </style>
        </head>
        <body>
            <a href="/{site_slug}" class="btn-volver">← Volver al inicio</a>
            <h1>{post.title}</h1>
            <p style="color: #64748b; font-size: 0.9em;">Publicado el: {post.created_at.strftime("%d/%m/%Y")}</p>
            
            {f'<img src="{post.featured_image}" alt="{post.title}">' if post.featured_image else ''}
            
            <div class="post-content">
                {post.content}
            </div>
        </body>
        </html>
    """)