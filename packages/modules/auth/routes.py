import sys
sys.path.insert(0, "/app")
sys.path.insert(0, "/app/packages")

from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Annotated

from app.db.database import get_db
from packages.core.models.site import Site
from packages.core.models.site_module import SiteModule
from packages.core.models.module import Module
from packages.modules.auth.models import SiteUser, AuthSession
from packages.modules.auth.schemas import (
    SiteUserRegister,
    SiteUserLogin,
    SiteUserResponse,
    TokenResponse,
    AuthConfigResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)
from packages.modules.auth.services import AuthService

router = APIRouter(prefix="/api/v1/sites/{site_id}/auth", tags=["site-auth"])

# 👇 CONSTANTE AÑADIDA PARA EVITAR TEXTOS DUPLICADOS
ERROR_SITIO_NO_ENCONTRADO = "Sitio no encontrado"

async def get_site_auth_module(db: AsyncSession, site_id: int) -> SiteModule | None:
    """Obtiene el site_module de auth para un sitio"""
    result = await db.execute(
        select(Module).where(Module.slug == "auth")
    )
    module = result.scalar_one_or_none()
    
    if not module:
        return None
    
    result = await db.execute(
        select(SiteModule).where(
            and_(
                SiteModule.site_id == site_id,
                SiteModule.module_id == module.id,
                SiteModule.is_active == True
            )
        )
    )
    return result.scalar_one_or_none()

# 👇 CORRECCIÓN: Documentar el error 404 en 'responses'
@router.get("/config", response_model=AuthConfigResponse, responses={404: {"description": ERROR_SITIO_NO_ENCONTRADO}})
async def get_auth_config(
    site_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(Site).where(Site.id == site_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    
    site_module = await get_site_auth_module(db, site_id)
    
    if not site_module or not site_module.config:
        return AuthConfigResponse(
            registration_fields=["email", "password"],
            custom_fields=[],
            require_verification=False
        )
    
    return AuthConfigResponse(**site_module.config)

# 👇 CORRECCIÓN: Documentar los errores 404 y 400 en 'responses'
@router.post("/register", response_model=SiteUserResponse, status_code=status.HTTP_201_CREATED, responses={404: {"description": ERROR_SITIO_NO_ENCONTRADO}, 400: {"description": "Error de validación o registro"}})
async def register(
    site_id: int,
    user_data: SiteUserRegister,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(Site).where(Site.id == site_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    
    service = AuthService(db, site_id)
    try:
        user = await service.register(user_data)
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# 👇 CORRECCIÓN: Documentar los errores 404 y 401 en 'responses'
@router.post("/login", responses={404: {"description": ERROR_SITIO_NO_ENCONTRADO}, 401: {"description": "Credenciales inválidas"}})
async def login(
    site_id: int,
    credentials: SiteUserLogin,
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(Site).where(Site.id == site_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    
    service = AuthService(db, site_id)
    user_agent = request.headers.get("user-agent")
    client_ip = request.client.host if request.client else None
    
    try:
        user, tokens = await service.login(credentials.email, credentials.password, user_agent, client_ip)
        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens["refresh_token"],
            "token_type": tokens["token_type"],
            "expires_in": tokens["expires_in"],
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "phone": user.phone,
                "custom_fields": user.custom_fields,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
        }
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/logout")
async def logout(
    site_id: int,
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return {"message": "Logged out"}
    
    service = AuthService(db, site_id)
    await service.logout(token)
    return {"message": "Logged out successfully"}

# 👇 CORRECCIÓN: Documentar el error 401 en 'responses'
@router.get("/me", response_model=SiteUserResponse, responses={401: {"description": "No autenticado o sesión expirada"}})
async def get_current_user(
    site_id: int,
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        raise HTTPException(status_code=401, detail="No autenticado")
    
    service = AuthService(db, site_id)
    user = await service.get_current_user(token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Sesión inválida o expirada")
    
    return user

# 👇 CORRECCIÓN: Documentar el error 404 en 'responses'
@router.post("/forgot-password", responses={404: {"description": ERROR_SITIO_NO_ENCONTRADO}})
async def forgot_password(
    site_id: int,
    data: ForgotPasswordRequest,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(select(Site).where(Site.id == site_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    
    service = AuthService(db, site_id)
    await service.forgot_password(data.email)
    
    return {"message": "Si el email existe, se enviará un enlace de recuperación"}

# 👇 CORRECCIÓN: Documentar el error 400 en 'responses'
@router.post("/reset-password", responses={400: {"description": "Token inválido o expirado"}})
async def reset_password(
    site_id: int,
    data: ResetPasswordRequest,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    service = AuthService(db, site_id)
    success = await service.reset_password(data.token, data.new_password)
    
    if not success:
        raise HTTPException(status_code=400, detail="Token inválido o expirado")
    
    return {"message": "Contraseña actualizada correctamente"}