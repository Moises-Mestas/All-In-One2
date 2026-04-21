import secrets
from datetime import datetime, timedelta, timezone # 👈 AÑADIDO: timezone
from typing import Optional
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_

from packages.modules.auth.models import SiteUser, AuthSession, PasswordResetToken

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: AsyncSession, site_id: int):
        self.db = db
        self.site_id = site_id

    async def register(self, user_data) -> SiteUser:
        result = await self.db.execute(
            select(SiteUser).where(
                and_(
                    SiteUser.site_id == self.site_id,
                    SiteUser.email == user_data.email
                )
            )
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            raise ValueError("El email ya está registrado en este sitio")

        user = SiteUser(
            site_id=self.site_id,
            email=user_data.email,
            password_hash=pwd_context.hash(user_data.password),
            first_name=getattr(user_data, 'first_name', None),
            last_name=getattr(user_data, 'last_name', None),
            phone=getattr(user_data, 'phone', None),
            custom_fields=getattr(user_data, 'custom_fields', {}) or {},
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def login(self, email: str, password: str, user_agent: str = None, ip: str = None):
        result = await self.db.execute(
            select(SiteUser).where(
                and_(
                    SiteUser.site_id == self.site_id,
                    SiteUser.email == email,
                    SiteUser.is_active == True
                )
            )
        )
        user = result.scalar_one_or_none()
        
        if not user or not pwd_context.verify(password, user.password_hash):
            raise ValueError("Email o contraseña incorrectos")

        tokens = await self._create_session(user, user_agent, ip)
        return user, tokens

    async def _create_session(self, user: SiteUser, user_agent: str, ip: str):
        access_token = secrets.token_urlsafe(32)
        refresh_token = secrets.token_urlsafe(32)
        # 👇 CORRECCIÓN: datetime.now(timezone.utc)
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)

        session = AuthSession(
            site_user_id=user.id,
            site_id=self.site_id,
            session_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
            user_agent=user_agent,
            ip_address=ip,
        )
        self.db.add(session)
        await self.db.commit()
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            # 👇 CORRECCIÓN: datetime.now(timezone.utc)
            "expires_in": int((expires_at - datetime.now(timezone.utc)).total_seconds())
        }

    async def logout(self, access_token: str) -> bool:
        result = await self.db.execute(
            select(AuthSession).where(AuthSession.session_token == access_token)
        )
        session = result.scalar_one_or_none()
        
        if session:
            session.is_active = False
            await self.db.commit()
            return True
        return False

    async def get_current_user(self, access_token: str) -> Optional[SiteUser]:
        result = await self.db.execute(
            select(AuthSession).where(
                and_(
                    AuthSession.session_token == access_token,
                    AuthSession.is_active == True,
                    # 👇 CORRECCIÓN: datetime.now(timezone.utc)
                    AuthSession.expires_at > datetime.now(timezone.utc)
                )
            )
        )
        session = result.scalar_one_or_none()
        
        if not session:
            return None
        
        result = await self.db.execute(
            select(SiteUser).where(SiteUser.id == session.site_user_id)
        )
        return result.scalar_one_or_none()

    async def refresh_tokens(self, refresh_token: str):
        result = await self.db.execute(
            select(AuthSession).where(
                and_(
                    AuthSession.refresh_token == refresh_token,
                    AuthSession.is_active == True
                )
            )
        )
        old_session = result.scalar_one_or_none()
        
        if not old_session:
            raise ValueError("Token de refresh inválido")

        result = await self.db.execute(
            select(SiteUser).where(SiteUser.id == old_session.site_user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            raise ValueError("Usuario no encontrado")

        old_session.is_active = False
        return await self._create_session(user, old_session.user_agent, old_session.ip_address)

    async def forgot_password(self, email: str) -> Optional[str]:
        result = await self.db.execute(
            select(SiteUser).where(
                and_(
                    SiteUser.site_id == self.site_id,
                    SiteUser.email == email
                )
            )
        )
        user = result.scalar_one_or_none()
        
        if not user:
            return None

        token = secrets.token_urlsafe(32)
        reset_record = PasswordResetToken(
            site_user_id=user.id,
            site_id=self.site_id,
            token=token,
            # 👇 CORRECCIÓN: datetime.now(timezone.utc)
            expires_at=datetime.now(timezone.utc) + timedelta(hours=24)
        )
        self.db.add(reset_record)
        await self.db.commit()
        
        return token

    async def reset_password(self, token: str, new_password: str) -> bool:
        result = await self.db.execute(
            select(PasswordResetToken).where(
                and_(
                    PasswordResetToken.token == token,
                    PasswordResetToken.used_at == None,
                    # 👇 CORRECCIÓN: datetime.now(timezone.utc)
                    PasswordResetToken.expires_at > datetime.now(timezone.utc)
                )
            )
        )
        reset_record = result.scalar_one_or_none()
        
        if not reset_record:
            return False

        result = await self.db.execute(
            select(SiteUser).where(SiteUser.id == reset_record.site_user_id)
        )
        user = result.scalar_one_or_none()
        
        if not user:
            return False

        user.password_hash = pwd_context.hash(new_password)
        # 👇 CORRECCIÓN: datetime.now(timezone.utc)
        reset_record.used_at = datetime.now(timezone.utc)
        
        await self.db.commit()
        return True