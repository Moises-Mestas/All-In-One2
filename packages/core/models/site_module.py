from sqlalchemy import ForeignKey, Boolean, JSON, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .site import Site
    from .module import Module

class SiteModule(Base, TimestampMixin):
    __tablename__ = "site_modules"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"), index=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id"), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    config: Mapped[dict] = mapped_column(JSON, default=dict)
    activated_at: Mapped[datetime | None] = mapped_column(nullable=True)
    deactivated_at: Mapped[datetime | None] = mapped_column(nullable=True)

    site: Mapped["Site"] = relationship("Site", back_populates="site_modules")
    module: Mapped["Module"] = relationship("Module", back_populates="site_modules")

    __table_args__ = (
        UniqueConstraint("site_id", "module_id"),
    )