from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import FastAPI
    from sqlalchemy.orm import Session


class Module(ABC):
    name: str = ""
    slug: str = ""
    version: str = "1.0.0"
    description: str = ""
    icon: str = "box"
    admin_url: str | None = None
    is_system: bool = False

    def __init__(self):
        self.routes_prefix = f"/api/{self.slug}"
        self.admin_prefix = f"/admin/{self.slug}"

    @abstractmethod
    def get_models(self):
        pass

    @abstractmethod
    def get_schemas(self):
        pass

    def on_activate(self, site_id: int, db: "Session", config: dict):
        # Método opcional. El módulo de tienda no requiere acciones adicionales al activarse.
        pass

    def on_deactivate(self, site_id: int, db: "Session"):
        # Método opcional. El módulo de tienda no requiere acciones adicionales al desactivarse.
        pass

    def on_install(self, db: "Session"):
        # Método opcional. El módulo de tienda no requiere acciones adicionales al instalarse.
        pass

    def get_admin_menu(self) -> list[dict]:
        return []