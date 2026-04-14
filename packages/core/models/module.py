
from sqlalchemy import String, Boolean, Text, JSON 
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from typing import Optional, List

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .site_module import SiteModule

class Module(Base, TimestampMixin):
    __tablename__ = "modules"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    version: Mapped[str] = mapped_column(String(20), default="1.0.0")
    is_system: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    icon: Mapped[str] = mapped_column(String(50), default="box")
    config_schema: Mapped[dict] = mapped_column(JSON, default=dict)
    admin_url: Mapped[str | None] = mapped_column(String(255), nullable=True)

    site_modules: Mapped[list["SiteModule"]] = relationship(
        "SiteModule",
        back_populates="module"
    )
