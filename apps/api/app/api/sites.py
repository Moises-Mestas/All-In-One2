import sys
import os
import copy
import uuid
import aiofiles

sys.path.insert(0, "/app")
sys.path.insert(0, "/app/packages")

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Annotated # 👈 AÑADIDO: Annotated
from sqlalchemy.orm.attributes import flag_modified

from app.db.database import get_db
from packages.core.models.user import User
from packages.core.models.site import Site
from app.core.security import get_current_user
from packages.core.schemas.site import SiteCreate, SiteResponse, SiteUpdate

router = APIRouter(prefix="/sites", tags=["sites"])

# 👇 CONSTANTE AÑADIDA PARA EVITAR TEXTO DUPLICADO
ERROR_SITE_NO_ENCONTRADO = "Site no encontrado"

@router.get("", response_model=List[SiteResponse])
async def list_sites(
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(
        select(Site).where(Site.user_id == current_user.id)
    )
    sites = result.scalars().all()
    return sites

# 🔥 AQUÍ ESTÁ TU CÓDIGO ORIGINAL QUE ASIGNA EL DUEÑO (user_id) Y CLONA LA PLANTILLA 🔥
@router.post("", response_model=SiteResponse, status_code=status.HTTP_201_CREATED, responses={400: {"description": "El slug ya está en uso"}})
async def create_site(
    site_data: SiteCreate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    # 1. Verificamos que el slug no exista
    result = await db.execute(select(Site).where(Site.slug == site_data.slug))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El slug ya está en uso"
        )
        
    # 2. Lógica de Clonación de Plantilla
    copied_settings = None
    if site_data.template_id:
        template_result = await db.execute(
            select(Site).where(Site.id == site_data.template_id)
        )
        template_site = template_result.scalar_one_or_none()
        
        if template_site and template_site.settings:
            copied_settings = copy.deepcopy(template_site.settings)
            
    # 3. Creamos el registro con tu usuario
    # Si es template, guardamos los settings del request
    # Si no, usamos los settings clonados de la plantilla
    final_settings = site_data.settings if site_data.is_template else copied_settings
    
    site = Site(
        name=site_data.name,
        slug=site_data.slug,
        user_id=current_user.id,
        is_template=site_data.is_template, 
        settings=final_settings
    )
    
    db.add(site)
    await db.commit()
    await db.refresh(site)
    return site

# 👇 CORRECCIÓN: Documentar 404 en 'responses'
@router.get("/{site_id}", response_model=SiteResponse, responses={404: {"description": ERROR_SITE_NO_ENCONTRADO}})
async def get_site(
    site_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(
        select(Site).where(Site.id == site_id, Site.user_id == current_user.id)
    )
    site = result.scalar_one_or_none()
    
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_SITE_NO_ENCONTRADO
        )
    return site

# 👇 CORRECCIÓN: Documentar 404 en 'responses'
@router.delete("/{site_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"description": ERROR_SITE_NO_ENCONTRADO}})
async def delete_site(
    site_id: int,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(
        select(Site).where(Site.id == site_id, Site.user_id == current_user.id)
    )
    site = result.scalar_one_or_none()
    
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_SITE_NO_ENCONTRADO
        )
    
    await db.delete(site)
    await db.commit()

# 👇 CORRECCIÓN: Documentar 404 en 'responses'
@router.put("/{site_id}", response_model=SiteResponse, responses={404: {"description": ERROR_SITE_NO_ENCONTRADO}})
async def update_site(
    site_id: int,
    site_update: SiteUpdate,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(
        select(Site).where(Site.id == site_id, Site.user_id == current_user.id) # 👈 Si no tiene user_id, aquí falla y da 404
    )
    site = result.scalar_one_or_none()
    
    if not site:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ERROR_SITE_NO_ENCONTRADO
        )
    
    if site_update.settings is not None:
        site.settings = site_update.settings
        flag_modified(site, "settings") 
    
    if site_update.name is not None:
        site.name = site_update.name
        
    if site_update.is_template is not None:
        site.is_template = site_update.is_template
        
    await db.commit()
    await db.refresh(site)
    return site

# 👇 CORRECCIÓN: Documentar 404 en 'responses'
@router.post("/{site_id}/upload-image", responses={404: {"description": ERROR_SITE_NO_ENCONTRADO}})
async def upload_site_image(
    site_id: int,
    file: Annotated[UploadFile, File(...)], # 👈 CORRECCIÓN: Annotated para File(...)
    current_user: Annotated[User, Depends(get_current_user)],
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Sube una imagen para el sitio y retorna la URL"""
    result = await db.execute(select(Site).where(Site.id == site_id, Site.user_id == current_user.id))
    site = result.scalar_one_or_none()
    
    if not site:
        raise HTTPException(status_code=404, detail=ERROR_SITE_NO_ENCONTRADO)
    
    ext = file.filename.split('.')[-1] if '.' in file.filename else 'jpg'
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = f"/app/uploads/{filename}"
    
    async with aiofiles.open(filepath, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    return {"url": f"/uploads/{filename}"}