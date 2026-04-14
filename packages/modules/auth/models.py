from sqlalchemy import String, ForeignKey, Boolean, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import uuid

from packages.core.models.base import Base, TimestampMixin

# 👇 CONSTANTES AÑADIDAS PARA EVITAR TEXTOS DUPLICADOS
SITES_ID_FK = "sites.id"
SITE_USERS_ID_FK = "site_users.id"

class SiteUser(Base, TimestampMixin):
    __tablename__ = "site_users"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey(SITES_ID_FK, ondelete="CASCADE"), index=True)
    
    email: Mapped[str] = mapped_column(String(255), index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    
    first_name: Mapped[str] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str] = mapped_column(String(100), nullable=True)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    
    custom_fields: Mapped[dict] = mapped_column(JSON, default=dict)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    verification_token: Mapped[str | None] = mapped_column(String(64), nullable=True)
    verified_at: Mapped[datetime | None] = mapped_column(nullable=True)

    __table_args__ = (
        {"sqlite_autoincrement": True},
    )

    def __repr__(self):
        return f"<SiteUser {self.email} (site={self.site_id})>"


class AuthSession(Base, TimestampMixin):
    __tablename__ = "auth_sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_user_id: Mapped[int] = mapped_column(ForeignKey(SITE_USERS_ID_FK, ondelete="CASCADE"), index=True)
    site_id: Mapped[int] = mapped_column(ForeignKey(SITES_ID_FK, ondelete="CASCADE"), index=True)
    
    session_token: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    refresh_token: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    
    expires_at: Mapped[datetime] = mapped_column()
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    
    user_agent: Mapped[str | None] = mapped_column(String(500), nullable=True)
    ip_address: Mapped[str | None] = mapped_column(String(45), nullable=True)

    __table_args__ = (
        {"sqlite_autoincrement": True},
    )

    def __repr__(self):
        return f"<AuthSession {self.id} (user={self.site_user_id})>"


class PasswordResetToken(Base, TimestampMixin):
    __tablename__ = "password_reset_tokens"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_user_id: Mapped[int] = mapped_column(ForeignKey(SITE_USERS_ID_FK, ondelete="CASCADE"), index=True)
    site_id: Mapped[int] = mapped_column(ForeignKey(SITES_ID_FK, ondelete="CASCADE"), index=True)
    
    token: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    expires_at: Mapped[datetime] = mapped_column()
    used_at: Mapped[datetime | None] = mapped_column(nullable=True)

    __table_args__ = (
        {"sqlite_autoincrement": True},
    )