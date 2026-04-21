import sys
sys.path.insert(0, "/app")
sys.path.insert(0, "/app/packages")

from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Annotated

from app.db.database import get_db
from packages.core.models.user import User
from packages.core.models.site_module import SiteModule
from packages.core.models.site import Site
from packages.core.models.module import Module
from packages.core.schemas.site_module import SiteModuleCreate, SiteModuleUpdate, SiteModuleResponse
from app.core.security import get_current_user

router = APIRouter(prefix="/site-modules", tags=["site-modules"])

# 👇 CONSTANTES AÑADIDAS PARA EVITAR TEXTOS DUPLICADOS
ERROR_SITIO_NO_ENCONTRADO = "Sitio no encontrado"
ERROR_SITE_MODULE_NO_ENCONTRADO = "SiteModule no encontrado"

# 👇 FIX BD: Función para obtener UTC compatible con tu base de datos (sin timezone info)
def get_utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)

@router.get("", response_model=List[SiteModuleResponse])
async def list_site_modules(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(
        select(SiteModule)
        .join(Site)
        .where(Site.user_id == current_user.id)
    )
    site_modules = result.scalars().all()
    return site_modules

# 👇 CORRECCIÓN: Documentar 404 en 'responses'
@router.get("/site/{site_id}", response_model=List[SiteModuleResponse], responses={404: {"description": ERROR_SITIO_NO_ENCONTRADO}})
async def get_site_modules(
    site_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result_site = await db.execute(
        select(Site).where(Site.id == site_id, Site.user_id == current_user.id)
    )
    if not result_site.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_SITIO_NO_ENCONTRADO
        )
        
    result = await db.execute(
        select(SiteModule).where(SiteModule.site_id == site_id)
    )
    site_modules = result.scalars().all()
    return site_modules

# 👇 CORRECCIÓN: Documentar 404 y 400 en 'responses'
@router.post("", response_model=SiteModuleResponse, status_code=status.HTTP_201_CREATED, responses={404: {"description": "Sitio o Módulo no encontrado"}, 400: {"description": "Este módulo ya está asignado a este sitio"}})
async def create_site_module(
    site_module_data: SiteModuleCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result_site = await db.execute(
        select(Site).where(Site.id == site_module_data.site_id, Site.user_id == current_user.id)
    )
    if not result_site.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_SITIO_NO_ENCONTRADO
        )
        
    result_module = await db.execute(
        select(Module).where(Module.id == site_module_data.module_id)
    )
    if not result_module.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Módulo no encontrado"
        )
        
    result_exists = await db.execute(
        select(SiteModule).where(
            SiteModule.site_id == site_module_data.site_id,
            SiteModule.module_id == site_module_data.module_id
        )
    )
    if result_exists.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este módulo ya está asignado a este sitio"
        )
        
    site_module = SiteModule(
        site_id=site_module_data.site_id,
        module_id=site_module_data.module_id,
        is_active=site_module_data.is_active,
        config=site_module_data.config,
        # 👇 APLICADO EL FIX AQUÍ
        activated_at=get_utc_now() if site_module_data.is_active else None,
    )
    db.add(site_module)
    await db.commit()
    await db.refresh(site_module)
    return site_module

# 👇 CORRECCIÓN: Documentar 404 en 'responses'
@router.post("/site/{site_id}/activate-module/{module_slug}", response_model=SiteModuleResponse, responses={404: {"description": "Sitio o Módulo no encontrado"}})
async def activate_module_for_site(
    site_id: int,
    module_slug: str,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Activa un módulo para un sitio, creándolo si no existe"""
    result_site = await db.execute(
        select(Site).where(Site.id == site_id, Site.user_id == current_user.id)
    )
    site = result_site.scalar_one_or_none()
    if not site:
        raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    
    result_module = await db.execute(
        select(Module).where(Module.slug == module_slug)
    )
    module = result_module.scalar_one_or_none()
    if not module:
        raise HTTPException(status_code=404, detail=f"Módulo '{module_slug}' no encontrado")
    
    result_exists = await db.execute(
        select(SiteModule).where(
            SiteModule.site_id == site_id,
            SiteModule.module_id == module.id
        )
    )
    existing = result_exists.scalar_one_or_none()
    
    default_config = {
        "registration_fields": ["email", "password", "first_name", "last_name", "phone"],
        "custom_fields": [],
        "require_verification": False
    }
    
    if existing:
        existing.is_active = True
        existing.config = default_config
        # 👇 APLICADO EL FIX AQUÍ
        existing.activated_at = get_utc_now()
        await db.commit()
        await db.refresh(existing)
        return existing
    else:
        new_sm = SiteModule(
            site_id=site_id,
            module_id=module.id,
            is_active=True,
            config=default_config,
            # 👇 APLICADO EL FIX AQUÍ
            activated_at=get_utc_now()
        )
        db.add(new_sm)
        await db.commit()
        await db.refresh(new_sm)
        return new_sm

# 👇 CORRECCIÓN: Documentar 404 en 'responses'
@router.put("/{site_module_id}", response_model=SiteModuleResponse, responses={404: {"description": ERROR_SITE_MODULE_NO_ENCONTRADO}})
async def update_site_module(
    site_module_id: int,
    site_module_update: SiteModuleUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(
        select(SiteModule)
        .join(Site)
        .where(SiteModule.id == site_module_id, Site.user_id == current_user.id)
    )
    site_module = result.scalar_one_or_none()
    
    if not site_module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_SITE_MODULE_NO_ENCONTRADO
        )
    
    if site_module_update.is_active is not None:
        site_module.is_active = site_module_update.is_active
        if site_module_update.is_active:
            # 👇 APLICADO EL FIX AQUÍ
            site_module.activated_at = get_utc_now()
        else:
            # 👇 APLICADO EL FIX AQUÍ
            site_module.deactivated_at = get_utc_now()
    
    if site_module_update.config is not None:
        site_module.config = site_module_update.config
        
    await db.commit()
    await db.refresh(site_module)
    return site_module

# 👇 CORRECCIÓN: Documentar 404 en 'responses'
@router.delete("/{site_module_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"description": ERROR_SITE_MODULE_NO_ENCONTRADO}})
async def delete_site_module(
    site_module_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(
        select(SiteModule)
        .join(Site)
        .where(SiteModule.id == site_module_id, Site.user_id == current_user.id)
    )
    site_module = result.scalar_one_or_none()
    
    if not site_module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_SITE_MODULE_NO_ENCONTRADO
        )
    
    await db.delete(site_module)
    await db.commit()

# 👇 CORRECCIÓN: Documentar 404 en 'responses'
@router.post("/{site_module_id}/toggle", response_model=SiteModuleResponse, responses={404: {"description": ERROR_SITE_MODULE_NO_ENCONTRADO}})
async def toggle_site_module(
    site_module_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(
        select(SiteModule)
        .join(Site)
        .where(SiteModule.id == site_module_id, Site.user_id == current_user.id)
    )
    site_module = result.scalar_one_or_none()
    
    if not site_module:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_SITE_MODULE_NO_ENCONTRADO
        )
    
    site_module.is_active = not site_module.is_active
    if site_module.is_active:
        # 👇 APLICADO EL FIX AQUÍ
        site_module.activated_at = get_utc_now()
    else:
        # 👇 APLICADO EL FIX AQUÍ
        site_module.deactivated_at = get_utc_now()
    
    await db.commit()
    await db.refresh(site_module)
    return site_module