from __future__ import annotations
from typing import Any, Dict, Optional, List, TYPE_CHECKING
from sqlalchemy import String, ForeignKey, JSON, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship 

from packages.core.models.base import BaseModel, TimestampMixin

# 👇 ESTA ES LA MAGIA QUE EVITA QUE SQLALCHEMY COLAPSE 👇
if TYPE_CHECKING:
    from packages.core.models.site_module import SiteModule
    from packages.core.models.user import User

class Site(BaseModel, TimestampMixin):
    __tablename__ = "sites"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    settings: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    is_template: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="sites")
    site_modules: Mapped[List["SiteModule"]] = relationship("SiteModule", back_populates="site", cascade="all, delete-orphan")