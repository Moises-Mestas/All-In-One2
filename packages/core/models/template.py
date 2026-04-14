from typing import Optional, Any
from sqlalchemy import String, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column

from packages.core.models.base import BaseModel, TimestampMixin

class Template(BaseModel, TimestampMixin):
    __tablename__ = "templates"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    # La configuración de GrapesJS (HTML, CSS, JSON)
    settings: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    
    # URL de una imagen en miniatura para mostrar en el frontend
    thumbnail_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)