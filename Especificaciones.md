# CMS Modular - Especificación Técnica Completa

## Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Arquitectura](#arquitectura)
3. [Stack Tecnológico](#stack-tecnológico)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Modelo de Datos](#modelo-de-datos)
6. [Sistema de Módulos](#sistema-de-módulos)
7. [Autenticación y Autorización](#autenticación-y-autorización)
8. [API REST](#api-rest)
9. [Frontend Admin Panel](#frontend-admin-panel)
10. [Plan de Desarrollo](#plan-de-desarrollo)
11. [Setup Inicial](#setup-inicial)

---

## Visión General

Plataforma web tipo CMS evolucionada con sistema modular inteligente que permite:

- Creación de sitios web desde panel centralizado
- Activación/desactivación de funcionalidades mediante "switches"
- Módulos independientes y desacoplados
- Multi-tenant (múltiples sitios con configuraciones distintas)
- Escalabilidad y mantenimiento sencillo

### Objetivos

1. Uso interno para desarrollo rápido de websites
2. eventual servicio SaaS multi-tenant
3. Extensible para funcionalidades empresariales

---

## Arquitectura

### Enfoque: Modular Monolith

Para este proyecto, se recomienda **no usar microservicios**. Un "Modular Monolith" es la mejor opción porque:

| Aspecto                  | Microservicios | Monolito Modular |
| ------------------------ | -------------- | ---------------- |
| Complejidad operacional  | Alta           | Baja             |
| Costo de infraestructura | Alto           | Bajo             |
| Debugging                | Difícil        | Sencillo         |
| Desarrollo inicial       | Lento          | Rápido           |
| Escalar después          | Sí es posible  | Sí es posible    |

### Diagrama de Arquitectura

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTE                                   │
│                    (Navegador / App)                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Next.js)                           │
│                                                                 │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐       │
│  │  Admin Panel │    │ Sites (gen)  │    │   Landing    │       │
│  │  /admin/*    │    │  /site/*     │    │     /        │       │
│  └──────────────┘    └──────────────┘    └──────────────┘       │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    API GATEWAY (FastAPI)                        │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    MIDDLEWARE                             │   │
│  │  • CORS      • Rate Limit    • Site Resolver             │   │
│  │  • Auth JWT  • Logging       • Error Handler              │   │
│  └──────────────────────────────────────────────────────────┘   │
│                              │                                  │
│  ┌────────────┬─────────────┴────────────┬────────────┐       │
│  │            │                          │            │       │
│  ▼            ▼                          ▼            ▼       │
│ ┌────────┐ ┌────────┐              ┌──────────┐ ┌──────────┐   │
│ │  Core  │ │ Module │              │  Module  │ │  Module  │   │
│ │        │ │   A    │              │    B     │ │    C     │   │
│ │ • Users│ │ (Blog) │              │ (Store)  │ │(Analytics)│  │
│ │ • Sites│ │        │              │          │ │          │   │
│ │ • Mods │ │        │              │          │ │          │   │
│ └────────┘ └────────┘              └──────────┘ └──────────┘   │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      DATA LAYER                                 │
│                                                                 │
│  ┌────────────┐    ┌────────────┐    ┌────────────┐            │
│  │ PostgreSQL │    │   Redis    │    │    S3      │            │
│  │  (datos)   │    │  (cache)   │    │  (files)   │            │
│  └────────────┘    └────────────┘    └────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Stack Tecnológico

### Backend

| Componente  | Tecnología   | Versión | Propósito               |
| ----------- | ------------ | ------- | ----------------------- |
| Framework   | FastAPI      | 0.109+  | API REST async          |
| ORM         | SQLAlchemy   | 2.0+    | Acceso a datos          |
| Validación  | Pydantic     | 2.0+    | Schemas y validación    |
| Migraciones | Alembic      | 1.13+   | Versionado de DB        |
| Auth        | python-jose  | 3.3+    | JWT tokens              |
| Password    | passlib      | 1.7+    | Hashing                 |
| Async DB    | asyncpg      | 0.29+   | Driver PostgreSQL async |
| Cache       | redis-py     | 5.0+    | Cache y sessions        |
| CORS        | fastapi-cors | -       | Cross-origin            |

### Frontend

| Componente | Tecnología      | Versión | Propósito         |
| ---------- | --------------- | ------- | ----------------- |
| Framework  | Next.js         | 14+     | React full-stack  |
| UI Library | shadcn/ui       | latest  | Componentes       |
| Estilos    | Tailwind CSS    | 3.4+    | CSS utility-first |
| Icons      | Lucide React    | latest  | Iconos            |
| State      | Zustand         | 4.4+    | Estado global     |
| Data Fetch | TanStack Query  | 5+      | Server state      |
| Forms      | React Hook Form | 7+      | Formularios       |
| Editor     | Tiptap          | 2.2+    | WYSIWYG           |

### Infraestructura

| Componente   | Tecnología     | Propósito               |
| ------------ | -------------- | ----------------------- |
| Containers   | Docker         | Empaquetado             |
| Orquestación | Docker Compose | Desarrollo local        |
| DB           | PostgreSQL     | Base de datos principal |
| Cache        | Redis          | Sesiones y cache        |
| Storage      | MinIO/S3       | Archivos estáticos      |
| Monorepo     | Turborepo      | Gestión multi-paquete   |

---

## Estructura del Proyecto

```
cms-platform/
│
├── apps/
│   ├── api/                          # Backend FastAPI
│   │   ├── main.py                   # Entry point
│   │   ├── config.py                # Configuración
│   │   ├── dependencies.py          # Inyección de dependencias
│   │   ├── middleware/               # Middlewares personalizados
│   │   │   ├── auth.py
│   │   │   ├── site.py
│   │   │   └── rate_limit.py
│   │   ├── routers/                  # Routers de la API
│   │   │   ├── core/
│   │   │   └── modules/
│   │   └── utils/
│   │
│   └── web/                          # Frontend Next.js (Admin)
│       ├── app/
│       │   ├── (auth)/              # Rutas de autenticación
│       │   │   ├── login/
│       │   │   └── register/
│       │   ├── (dashboard)/          # Rutas protegidas
│       │   │   ├── layout.tsx
│       │   │   ├── page.tsx
│       │   │   ├── sites/
│       │   │   ├── modules/
│       │   │   ├── users/
│       │   │   └── settings/
│       │   └── api/                  # API routes del cliente
│       ├── components/
│       │   ├── ui/                  # shadcn/ui components
│       │   ├── admin/               # Componentes del admin
│       │   └── module-renderer/     # Renderizado dinámico
│       ├── lib/
│       │   ├── api.ts               # Cliente API
│       │   └── utils.ts
│       └── hooks/                    # Custom hooks
│
├── packages/
│   │
│   ├── core/                        # Núcleo del sistema
│   │   ├── __init__.py
│   │   ├── database.py              # Configuración SQLAlchemy
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # BaseModel
│   │   │   ├── user.py              # User model
│   │   │   ├── site.py              # Site model
│   │   │   ├── module.py            # Module model
│   │   │   └── site_module.py       # SiteModule (pivot)
│   │   ├── schemas/
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── site.py
│   │   │   └── module.py
│   │   ├── services/
│   │   │   ├── user_service.py
│   │   │   ├── site_service.py
│   │   │   └── module_service.py
│   │   └── plugin_base.py           # Clase base para módulos
│   │
│   ├── modules/                     # Módulos del sistema
│   │   │
│   │   ├── auth/                    # Módulo de autenticación
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── routes.py
│   │   │   ├── services.py
│   │   │   └── templates/           # Templates de email
│   │   │
│   │   ├── blog/                    # Módulo de blog
│   │   │   ├── __init__.py
│   │   │   ├── models.py            # Post, Category, Tag
│   │   │   ├── schemas.py
│   │   │   ├── routes.py
│   │   │   ├── services.py
│   │   │   └── migrations/
│   │   │
│   │   ├── store/                   # Módulo de tienda
│   │   │   ├── __init__.py
│   │   │   ├── models.py            # Product, Order, Cart
│   │   │   ├── schemas.py
│   │   │   ├── routes.py
│   │   │   └── services.py
│   │   │
│   │   ├── inventory/               # Módulo de inventario
│   │   │   ├── __init__.py
│   │   │   ├── models.py            # Stock, Warehouse
│   │   │   ├── schemas.py
│   │   │   ├── routes.py
│   │   │   └── services.py
│   │   │
│   │   └── analytics/               # Módulo de analítica
│   │       ├── __init__.py
│   │       ├── models.py            # Event, Report
│   │       ├── schemas.py
│   │       ├── routes.py
│   │       └── services.py
│   │
│   ├── shared/                      # Código compartido
│   │   ├── utils/
│   │   │   ├── response.py          # Respuestas estándar
│   │   │   ├── exceptions.py        # Excepciones personalizadas
│   │   │   └── pagination.py        # Helper de paginación
│   │   ├── constants.py
│   │   └── types.py
│   │
│   └── ui/                          # Componentes compartidos
│       ├── button/
│       ├── card/
│       ├── input/
│       └── dialog/
│
├── docker/
│   ├── api.Dockerfile
│   ├── web.Dockerfile
│   └── nginx.conf
│
├── docker-compose.yml
├── turbo.json
├── package.json
├── pnpm-workspace.yaml
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Modelo de Datos

### Diagrama ER

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           ENTIDADES PRINCIPALES                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│    ┌─────────────┐         ┌─────────────────┐         ┌─────────────┐  │
│    │    USER     │         │      SITE       │         │   MODULE    │  │
│    ├─────────────┤         ├─────────────────┤         ├─────────────┤  │
│    │ id (PK)     │         │ id (PK)         │         │ id (PK)     │  │
│    │ email       │         │ name            │         │ name        │  │
│    │ password    │         │ slug            │         │ slug        │  │
│    │ first_name  │         │ domain          │         │ description │  │
│    │ last_name   │         │ settings (JSON)  │         │ version     │  │
│    │ role        │         │ theme           │         │ is_system   │  │
│    │ is_active   │         │ is_active       │         │ config_schema│ │
│    │ created_at  │         │ created_at      │         │ created_at  │  │
│    │ updated_at  │         │ updated_at      │         │ updated_at  │  │
│    └─────────────┘         └─────────────────┘         └─────────────┘  │
│           │                        │                        │            │
│           │                        │                        │            │
│           │    ┌───────────────────┘                        │            │
│           │    │                                            │            │
│           ▼    ▼                                            │            │
│    ┌─────────────────────────────────┐                       │            │
│    │        SITE_MODULE             │◄──────────────────────┘            │
│    ├─────────────────────────────────┤     (FK: module_id)               │
│    │ id (PK)                         │                                     │
│    │ site_id (FK)                    │◄───────────┐                       │
│    │ module_id (FK)                  │            │                       │
│    │ is_active                       │            │                       │
│    │ config (JSON)                   │     ┌──────┴────────┐              │
│    │ activated_at                    │     │    (FK: site_id)              │
│    │ deactivated_at                  │     │              │              │
│    └─────────────────────────────────┘     ▼              ▼              │
│                                              (1)           (1)            │
│                                         ┌────────┐   ┌───────────┐        │
│                                         │  USER  │   │   SITE    │        │
│                                         │(admin) │   │           │        │
│                                         └────────┘   └───────────┘        │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────────────┐
│                           MÓDULOS ESPECÍFICOS                           │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐        │
│  │      POST       │  │    PRODUCT      │  │     ORDER       │        │
│  ├─────────────────┤  ├─────────────────┤  ├─────────────────┤        │
│  │ id              │  │ id              │  │ id              │        │
│  │ site_id (FK)    │  │ site_id (FK)    │  │ site_id (FK)    │        │
│  │ title           │  │ name            │  │ order_number    │        │
│  │ slug            │  │ sku             │  │ user_id (FK)    │        │
│  │ content         │  │ description     │  │ status          │        │
│  │ excerpt         │  │ price           │  │ subtotal        │        │
│  │ featured_image  │  │ compare_price   │  │ tax             │        │
│  │ status          │  │ cost            │  │ total           │        │
│  │ author_id (FK)  │  │ stock_quantity  │  │ shipping_address│        │
│  │ category_id(FK) │  │ is_active       │  │ payment_method  │        │
│  │ published_at    │  │ images (JSON)   │  │ payment_status  │        │
│  │ created_at      │  │ variants (JSON) │  │ created_at      │        │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘        │
│         │                                        │                      │
│         │              ┌─────────────────┐       │                      │
│         └────────────►│    CATEGORY     │◄──────┘                      │
│                        ├─────────────────┤        ┌─────────────────┐  │
│                        │ id              │        │   ORDER_ITEM    │  │
│                        │ site_id (FK)    │        ├─────────────────┤  │
│                        │ parent_id (FK)  │        │ id              │  │
│                        │ name            │        │ order_id (FK)   │  │
│                        │ slug            │        │ product_id (FK) │  │
│                        │ description     │        │ quantity        │  │
│                        │ image           │        │ price           │  │
│                        │ order           │        │ total           │  │
│                        └─────────────────┘        └─────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Models SQLAlchemy

#### Core Models

```python
# packages/core/models/base.py
from datetime import datetime
from typing import Optional
from sqlalchemy import DateTime, Boolean, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )


class SoftDeleteMixin:
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
```

```python
# packages/core/models/user.py
from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
import enum

from .base import Base, TimestampMixin, SoftDeleteMixin

if TYPE_CHECKING:
    from .site import Site

class UserRole(str, enum.Enum):
    SUPER_ADMIN = "super_admin"
    SITE_ADMIN = "site_admin"
    EDITOR = "editor"
    VIEWER = "viewer"


class User(Base, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    role: Mapped[UserRole] = mapped_column(
        SQLEnum(UserRole),
        default=UserRole.VIEWER
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    avatar_url: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Relations
    site_id: Mapped[int | None] = mapped_column(
        ForeignKey("sites.id"),
        nullable=True
    )
    site: Mapped["Site"] = relationship("Site", back_populates="users")
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author")
```

```python
# packages/core/models/site.py
from sqlalchemy import String, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from .base import Base, TimestampMixin

if TYPE_CHECKING:
    from .user import User
    from .site_module import SiteModule

class Site(Base, TimestampMixin):
    __tablename__ = "sites"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    domain: Mapped[str | None] = mapped_column(String(255), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    settings: Mapped[dict] = mapped_column(JSON, default=dict)
    theme: Mapped[str] = mapped_column(String(100), default="default")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relations
    users: Mapped[list["User"]] = relationship("User", back_populates="site")
    site_modules: Mapped[list["SiteModule"]] = relationship(
        "SiteModule",
        back_populates="site",
        cascade="all, delete-orphan"
    )
```

```python
# packages/core/models/module.py
from sqlalchemy import String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

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

    # Relations
    site_modules: Mapped[list["SiteModule"]] = relationship(
        "SiteModule",
        back_populates="module"
    )
```

```python
# packages/core/models/site_module.py
from sqlalchemy import ForeignKey, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from typing import TYPE_CHECKING
import enum

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

    # Relations
    site: Mapped["Site"] = relationship("Site", back_populates="site_modules")
    module: Mapped["Module"] = relationship("Module", back_populates="site_modules")

    __table_args__ = (
        UniqueConstraint("site_id", "module_id"),
    )
```

---

## Sistema de Módulos

### Concepto

Cada módulo es un paquete Python independiente que:

1. Define sus propios modelos de datos
2. Registra sus propias rutas de API
3. Provee su propia configuración
4. Se activa/desactiva dinámicamente

### Clase Base del Módulo

```python
# packages/core/plugin_base.py
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from fastapi import FastAPI
    from sqlalchemy.orm import Session

class Module(ABC):
    """Clase base que todos los módulos deben implementar."""

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
        """Retorna las clases de modelos SQLAlchemy del módulo."""
        pass

    @abstractmethod
    def get_schemas(self):
        """Retorna los schemas Pydantic del módulo."""
        pass

    def on_activate(self, site_id: int, db: Session, config: dict):
        """Hook ejecutado cuando el módulo se activa."""
        pass

    def on_deactivate(self, site_id: int, db: Session):
        """Hook ejecutado cuando el módulo se desactiva."""
        pass

    def on_install(self, db: Session):
        """Hook ejecutado cuando el módulo se instala en el sistema."""
        pass

    def get_admin_menu(self) -> list[dict]:
        """Retorna items del menú de administración."""
        return []
```

### Ejemplo: Módulo Blog

```python
# packages/modules/blog/__init__.py
from core.plugin_base import Module
from .models import Post, Category, Tag, PostTag
from .schemas import (
    PostSchema,
    PostCreate,
    PostUpdate,
    CategorySchema,
    CategoryCreate,
)

class BlogModule(Module):
    name = "Blog"
    slug = "blog"
    version = "1.0.0"
    description = "Sistema de gestión de contenidos y blog"
    icon = "file-text"
    admin_url = "/admin/blog"

    def get_models(self):
        return [Post, Category, Tag, PostTag]

    def get_schemas(self):
        return {
            "Post": PostSchema,
            "PostCreate": PostCreate,
            "PostUpdate": PostUpdate,
            "Category": CategorySchema,
            "CategoryCreate": CategoryCreate,
        }

    def on_activate(self, site_id: int, db: Session, config: dict):
        """Crear estructura inicial del blog."""
        default_category = Category(
            site_id=site_id,
            name="General",
            slug="general",
            description="Categoría por defecto"
        )
        db.add(default_category)
        db.commit()

    def get_admin_menu(self) -> list[dict]:
        return [
            {
                "title": "Artículos",
                "url": f"{self.admin_url}/posts",
                "icon": self.icon,
                "children": [
                    {"title": "Todos los artículos", "url": f"{self.admin_url}/posts"},
                    {"title": "Nueva entrada", "url": f"{self.admin_url}/posts/new"},
                    {"title": "Categorías", "url": f"{self.admin_url}/categories"},
                    {"title": "Etiquetas", "url": f"{self.admin_url}/tags"},
                ]
            }
        ]


# Registrar el módulo
module = BlogModule()
```

```python
# packages/modules/blog/models.py
from sqlalchemy import String, Text, ForeignKey, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.models.base import Base, TimestampMixin

# Tabla muchos a muchos
post_tags = Table(
    "blog_post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("blog_posts.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("blog_tags.id"), primary_key=True),
)

class PostStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    SCHEDULED = "scheduled"
    ARCHIVED = "archived"


class Post(Base, TimestampMixin):
    __tablename__ = "blog_posts"
    __table_args__ = {"schema": None}  # Se filtra por site_id en queries

    id: Mapped[int] = mapped_column(primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"), index=True)
    title: Mapped[str] = mapped_column(String(500))
    slug: Mapped[str] = mapped_column(String(500), index=True)
    content: Mapped[str] = mapped_column(Text)
    excerpt: Mapped[str | None] = mapped_column(Text, nullable=True)
    featured_image: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[PostStatus] = mapped_column(
        SQLEnum(PostStatus),
        default=PostStatus.DRAFT
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("blog_categories.id"),
        nullable=True
    )
    published_at: Mapped[datetime | None] = mapped_column(nullable=True)
    seo_title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    seo_description: Mapped[str | None] = mapped_column(Text, nullable=True)

    author: Mapped["User"] = relationship("User", back_populates="posts")
    category: Mapped["Category"] = relationship("Category", back_populates="posts")
    tags: Mapped[list["Tag"]] = relationship("Tag", secondary=post_tags)
    comments: Mapped[list["Comment"]] = relationship("Comment", cascade="all, delete-orphan")


class Category(Base, TimestampMixin):
    __tablename__ = "blog_categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"), index=True)
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey("blog_categories.id"),
        nullable=True
    )
    name: Mapped[str] = mapped_column(String(100))
    slug: Mapped[str] = mapped_column(String(100), index=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    image: Mapped[str | None] = mapped_column(String(500), nullable=True)
    order: Mapped[int] = mapped_column(default=0)

    parent: Mapped["Category | None"] = relationship(
        "Category",
        remote_side=[id],
        back_populates="children"
    )
    children: Mapped[list["Category"]] = relationship("Category", back_populates="parent")
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="category")


class Tag(Base, TimestampMixin):
    __tablename__ = "blog_tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_id: Mapped[int] = mapped_column(ForeignKey("sites.id"), index=True)
    name: Mapped[str] = mapped_column(String(100))
    slug: Mapped[str] = mapped_column(String(100), index=True)

    posts: Mapped[list["Post"]] = relationship("Post", secondary=post_tags)
```

### Registry de Módulos

```python
# packages/core/module_registry.py
from typing import Type
from fastapi import FastAPI
from sqlalchemy.orm import Session

from .models import Module as ModuleModel, SiteModule
from .plugin_base import Module

class ModuleRegistry:
    """Registro central de todos los módulos del sistema."""

    _modules: dict[str, Type[Module]] = {}
    _instances: dict[str, Module] = {}

    @classmethod
    def register(cls, module_class: Type[Module]):
        """Registra un nuevo módulo."""
        instance = module_class()
        cls._modules[instance.slug] = module_class
        cls._instances[instance.slug] = instance
        return module_class

    @classmethod
    def get_module(cls, slug: str) -> Module | None:
        """Obtiene una instancia del módulo por slug."""
        return cls._instances.get(slug)

    @classmethod
    def get_all_modules(cls) -> list[Module]:
        """Obtiene todos los módulos registrados."""
        return list(cls._instances.values())

    @classmethod
    def get_active_modules(cls, site_id: int, db: Session) -> list[Module]:
        """Obtiene los módulos activos para un sitio."""
        active_slugs = (
            db.query(SiteModule)
            .filter(
                SiteModule.site_id == site_id,
                SiteModule.is_active == True
            )
            .all()
        )
        return [
            cls._instances.get(sm.module.slug)
            for sm in active_slugs
            if sm.module.slug in cls._instances
        ]

    @classmethod
    def activate_module(cls, site_id: int, module_slug: str, db: Session, config: dict = None):
        """Activa un módulo para un sitio."""
        module = cls.get_module(module_slug)
        if not module:
            raise ValueError(f"Módulo {module_slug} no encontrado")

        # Crear registro en site_modules
        site_module = SiteModule(
            site_id=site_id,
            module_id=db.query(ModuleModel).filter_by(slug=module_slug).first().id,
            is_active=True,
            config=config or {},
            activated_at=datetime.utcnow()
        )
        db.add(site_module)

        # Ejecutar hook de activación
        module.on_activate(site_id, db, config or {})
        db.commit()

    @classmethod
    def deactivate_module(cls, site_id: int, module_slug: str, db: Session):
        """Desactiva un módulo para un sitio."""
        module = cls.get_module(module_slug)
        if not module:
            return

        site_module = (
            db.query(SiteModule)
            .filter(
                SiteModule.site_id == site_id,
                SiteModule.module.has(slug=module_slug)
            )
            .first()
        )
        if site_module:
            site_module.is_active = False
            site_module.deactivated_at = datetime.utcnow()
            module.on_deactivate(site_id, db)
            db.commit()

    @classmethod
    def include_routes(cls, app: FastAPI):
        """Incluye las rutas de todos los módulos en la app."""
        for module in cls._instances.values():
            router = module.get_router()
            if router:
                app.include_router(
                    router,
                    prefix=module.routes_prefix,
                    tags=[module.name]
                )

    @classmethod
    def get_admin_menu(cls, site_id: int, db: Session) -> list[dict]:
        """Genera el menú de administración completo."""
        active_modules = cls.get_active_modules(site_id, db)
        menu = []

        # Core menu items
        menu.extend([
            {"title": "Dashboard", "url": "/admin", "icon": "layout-dashboard"},
            {"title": "Sitios", "url": "/admin/sites", "icon": "globe"},
            {"title": "Módulos", "url": "/admin/modules", "icon": "puzzle"},
            {"title": "Usuarios", "url": "/admin/users", "icon": "users"},
        ])

        # Module-specific menu items
        for module in active_modules:
            menu.extend(module.get_admin_menu())

        return menu


# Registrar módulos del sistema
from packages.modules.blog import BlogModule
from packages.modules.store import StoreModule
from packages.modules.inventory import InventoryModule
from packages.modules.analytics import AnalyticsModule

ModuleRegistry.register(BlogModule)
ModuleRegistry.register(StoreModule)
ModuleRegistry.register(InventoryModule)
ModuleRegistry.register(AnalyticsModule)
```

---

## Autenticación y Autorización

### Sistema de Auth

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUJO DE AUTENTICACIÓN                   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│   1. LOGIN                                                  │
│   ┌─────────┐      ┌─────────┐      ┌─────────┐           │
│   │  Login  │ ───► │  API    │ ───► │ Validate│           │
│   │  Form   │      │ /login  │      │  creds  │           │
│   └─────────┘      └────┬────┘      └────┬────┘           │
│                          │                 │                │
│                          ▼                 ▼                │
│                    ┌──────────┐      ┌──────────┐          │
│                    │  Redis   │      │   DB     │          │
│                    │ (session)│      │(password)│          │
│                    └──────────┘      └──────────┘          │
│                          │                                │
│                          ▼                                │
│                    ┌──────────┐                           │
│                    │ JWT      │                           │
│                    │ tokens   │                           │
│                    └────┬─────┘                           │
│                         │                                 │
│   2. ACCESO A RECURSOS                                     │
│   ┌─────────┐      ┌────┴────┐      ┌─────────────┐      │
│   │ Request │ ───► │ Check   │ ───► │   Allow/    │      │
│   │ + JWT   │      │  JWT    │      │   Deny      │      │
│   └─────────┘      └────┬────┘      └─────────────┘      │
│                         │                                   │
│                         ▼                                   │
│                    ┌──────────┐                            │
│                    │   DB     │                            │
│                    │(site_id) │                            │
│                    └──────────┘                            │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Implementación

```python
# apps/api/auth.py
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core.database import get_db
from core.models import User, UserRole

# Config
SECRET_KEY = os.getenv("JWT_SECRET", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Obtiene el usuario actual desde el token JWT."""
    token = credentials.credentials
    payload = decode_token(token)

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de acceso inválido"
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token malformado"
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado o inactivo"
        )

    return user


def require_roles(*roles: UserRole):
    """Decorator para requerir roles específicos."""
    async def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permisos para acceder a este recurso"
            )
        return current_user
    return role_checker


require_super_admin = require_roles(UserRole.SUPER_ADMIN)
require_admin = require_roles(UserRole.SUPER_ADMIN, UserRole.SITE_ADMIN)
```

```python
# apps/api/middleware/site.py
from fastapi import Request
from sqlalchemy.orm import Session

from core.database import get_db
from core.models import Site

async def site_middleware(request: Request, call_next):
    """Extrae el site_id del host o subdomain."""
    host = request.headers.get("host", "")

    # Parsear subdomain
    parts = host.split(".")
    if len(parts) >= 3:  # subdomain.domain.com
        subdomain = parts[0]
        # Buscar site por subdomain
        db_gen = get_db()
        db = next(db_gen)
        try:
            site = db.query(Site).filter(Site.slug == subdomain).first()
            if site:
                request.state.site_id = site.id
                request.state.site = site
        finally:
            db_gen.close()

    response = await call_next(request)
    return response
```

### Roles y Permisos

```python
class Permission(str, enum.Enum):
    # Site management
    MANAGE_SITES = "manage_sites"
    MANAGE_USERS = "manage_users"

    # Module management
    ACTIVATE_MODULES = "activate_modules"

    # Content
    CREATE_CONTENT = "create_content"
    EDIT_CONTENT = "edit_content"
    DELETE_CONTENT = "delete_content"
    PUBLISH_CONTENT = "publish_content"

    # Store
    MANAGE_PRODUCTS = "manage_products"
    MANAGE_ORDERS = "manage_orders"
    VIEW_REPORTS = "view_reports"


ROLE_PERMISSIONS = {
    UserRole.SUPER_ADMIN: [
        # Todos los permisos
    ],
    UserRole.SITE_ADMIN: [
        Permission.MANAGE_USERS,
        Permission.ACTIVATE_MODULES,
        Permission.CREATE_CONTENT,
        Permission.EDIT_CONTENT,
        Permission.DELETE_CONTENT,
        Permission.PUBLISH_CONTENT,
        Permission.MANAGE_PRODUCTS,
        Permission.MANAGE_ORDERS,
        Permission.VIEW_REPORTS,
    ],
    UserRole.EDITOR: [
        Permission.CREATE_CONTENT,
        Permission.EDIT_CONTENT,
        Permission.PUBLISH_CONTENT,
    ],
    UserRole.VIEWER: [],  # Solo lectura
}
```

---

## API REST

### Estructura de Endpoints

```
API_BASE: /api/v1

┌─────────────────────────────────────────────────────────────────┐
│                         CORE API                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  AUTH                                                           │
│  POST   /auth/login                    Login                    │
│  POST   /auth/register                 Registro                  │
│  POST   /auth/refresh                  Refrescar token          │
│  POST   /auth/logout                   Logout                    │
│  GET    /auth/me                       Usuario actual           │
│  POST   /auth/change-password          Cambiar password        │
│  POST   /auth/forgot-password          Olvidé password          │
│  POST   /auth/reset-password           Reset password          │
│                                                                  │
│  USERS                                                          │
│  GET    /users                         Listar usuarios          │
│  POST   /users                         Crear usuario           │
│  GET    /users/{id}                    Ver usuario             │
│  PUT    /users/{id}                    Actualizar usuario      │
│  DELETE /users/{id}                    Eliminar usuario        │
│                                                                  │
│  SITES                                                          │
│  GET    /sites                         Listar sitios           │
│  POST   /sites                         Crear sitio             │
│  GET    /sites/{id}                    Ver sitio               │
│  PUT    /sites/{id}                    Actualizar sitio        │
│  DELETE /sites/{id}                    Eliminar sitio          │
│  GET    /sites/{id}/config             Config del sitio        │
│  PUT    /sites/{id}/config             Guardar config          │
│                                                                  │
│  MODULES                                                        │
│  GET    /modules                       Listar módulos          │
│  GET    /modules/{slug}                Ver módulo              │
│  GET    /sites/{site_id}/modules       Módulos del sitio      │
│  POST   /sites/{site_id}/modules/{slug}/activate              │
│  POST   /sites/{site_id}/modules/{slug}/deactivate            │
│  GET    /sites/{site_id}/modules/{slug}/config                │
│  PUT    /sites/{site_id}/modules/{slug}/config                │
│                                                                  │
│  ADMIN MENU                                                     │
│  GET    /admin/menu                    Menú de administración  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│                      MODULE APIs                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  BLOG MODULE                                                    │
│  ─────────────                                                  │
│  GET    /blog/posts                     Listar posts            │
│  POST   /blog/posts                     Crear post              │
│  GET    /blog/posts/{id}                Ver post                │
│  PUT    /blog/posts/{id}                Actualizar post        │
│  DELETE /blog/posts/{id}                Eliminar post          │
│  POST   /blog/posts/{id}/publish        Publicar post          │
│  POST   /blog/posts/{id}/unpublish      Despublicar            │
│  GET    /blog/categories                Listar categorías      │
│  POST   /blog/categories                Crear categoría        │
│  GET    /blog/tags                      Listar etiquetas       │
│                                                                  │
│  STORE MODULE                                                    │
│  ─────────────                                                  │
│  GET    /store/products                 Listar productos       │
│  POST   /store/products                 Crear producto         │
│  GET    /store/products/{id}            Ver producto           │
│  PUT    /store/products/{id}            Actualizar producto    │
│  DELETE /store/products/{id}            Eliminar producto      │
│  GET    /store/orders                   Listar pedidos         │
│  GET    /store/orders/{id}              Ver pedido              │
│  PUT    /store/orders/{id}/status       Actualizar estado      │
│  POST   /store/cart                     Ver/crear carrito       │
│  POST   /store/cart/items               Agregar al carrito     │
│  POST   /store/checkout                  Checkout               │
│                                                                  │
│  INVENTORY MODULE                                               │
│  ─────────────────                                              │
│  GET    /inventory/stock                 Ver stock              │
│  GET    /inventory/alerts                Ver alertas            │
│  POST   /inventory/adjustments            Ajuste de stock       │
│  GET    /inventory/report                Reporte               │
│                                                                  │
│  ANALYTICS MODULE                                               │
│  ───────────────                                                │
│  GET    /analytics/dashboard             Dashboard              │
│  GET    /analytics/pageviews              Pageviews             │
│  GET    /analytics/visitors              Visitantes            │
│  GET    /analytics/conversions           Conversiones          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Response Format

```python
# packages/shared/utils/response.py
from typing import TypeVar, Generic, Optional
from pydantic import BaseModel

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Respuesta estándar de la API."""
    success: bool = True
    message: str = "OK"
    data: Optional[T] = None
    errors: Optional[list[dict]] = None
    meta: Optional[dict] = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Respuesta paginada."""
    success: bool = True
    data: list[T]
    meta: dict = {
        "total": 0,
        "page": 1,
        "per_page": 20,
        "total_pages": 0,
    }


class ErrorResponse(BaseModel):
    """Respuesta de error."""
    success: bool = False
    error: str
    detail: Optional[str] = None
    code: Optional[str] = None
```

```python
# Ejemplo de uso en routers
@router.get("/posts", response_model=PaginatedResponse[PostSchema])
async def list_posts(
    page: int = 1,
    per_page: int = 20,
    status: Optional[str] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db),
    site_id: int = Depends(get_current_site_id),
):
    query = db.query(Post).filter(Post.site_id == site_id)

    if status:
        query = query.filter(Post.status == status)
    if category_id:
        query = query.filter(Post.category_id == category_id)

    total = query.count()
    posts = query.offset((page - 1) * per_page).limit(per_page).all()

    return PaginatedResponse(
        data=[PostSchema.model_validate(p) for p in posts],
        meta={
            "total": total,
            "page": page,
            "per_page": per_page,
            "total_pages": (total + per_page - 1) // per_page,
        }
    )
```

---

## Frontend Admin Panel

### Estructura de Rutas

```
apps/web/
├── app/
│   ├── (auth)/
│   │   ├── login/
│   │   │   └── page.tsx
│   │   ├── register/
│   │   │   └── page.tsx
│   │   └── layout.tsx
│   │
│   ├── (dashboard)/
│   │   ├── layout.tsx              # Layout con sidebar
│   │   ├── page.tsx                # Dashboard
│   │   │
│   │   ├── sites/
│   │   │   ├── page.tsx           # Lista de sitios
│   │   │   ├── new/
│   │   │   │   └── page.tsx       # Crear sitio
│   │   │   └── [id]/
│   │   │       ├── page.tsx       # Editar sitio
│   │   │       └── settings/
│   │   │           └── page.tsx   # Settings del sitio
│   │   │
│   │   ├── modules/
│   │   │   ├── page.tsx           # Lista de módulos
│   │   │   └── [slug]/
│   │   │       └── page.tsx      # Configurar módulo
│   │   │
│   │   ├── users/
│   │   │   ├── page.tsx           # Lista de usuarios
│   │   │   ├── new/
│   │   │   │   └── page.tsx       # Crear usuario
│   │   │   └── [id]/
│   │   │       └── page.tsx      # Editar usuario
│   │   │
│   │   ├── blog/                  # Rutas dinámicas
│   │   │   ├── page.tsx          # Lista de posts
│   │   │   ├── new/
│   │   │   │   └── page.tsx      # Crear post
│   │   │   ├── [id]/
│   │   │   │   └── page.tsx      # Editar post
│   │   │   ├── categories/
│   │   │   │   └── page.tsx
│   │   │   └── tags/
│   │   │       └── page.tsx
│   │   │
│   │   ├── store/                 # Rutas dinámicas
│   │   │   ├── page.tsx          # Dashboard store
│   │   │   ├── products/
│   │   │   ├── orders/
│   │   │   └── customers/
│   │   │
│   │   └── settings/
│   │       ├── page.tsx          # Settings generales
│   │       ├── profile/
│   │       │   └── page.tsx
│   │       ├── security/
│   │       │   └── page.tsx
│   │       └── api-keys/
│   │           └── page.tsx
│   │
│   └── api/
│       └── [...slug]/
│           └── route.ts          # Proxy a API backend
│
├── components/
│   ├── ui/                       # shadcn/ui
│   ├── admin/
│   │   ├── sidebar.tsx          # Sidebar navigation
│   │   ├── header.tsx           # Header with user menu
│   │   ├── data-table.tsx       # Tabla genérica
│   │   └── module-card.tsx      # Card de módulo
│   └── module-renderer/
│       └── dynamic-module.tsx   # Renderiza módulos dinámicos
│
└── lib/
    ├── api.ts                   # Cliente de API
    ├── auth.ts                  # Helpers de auth
    └── utils.ts
```

### Layout Principal

```tsx
// apps/web/app/(dashboard)/layout.tsx
import { redirect } from "next/navigation";
import { Sidebar } from "@/components/admin/sidebar";
import { Header } from "@/components/admin/header";
import { getCurrentUser } from "@/lib/auth";

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const user = await getCurrentUser();

  if (!user) {
    redirect("/login");
  }

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header user={user} />
        <main className="flex-1 overflow-y-auto p-6">{children}</main>
      </div>
    </div>
  );
}
```

```tsx
// apps/web/components/admin/sidebar.tsx
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import { adminMenu } from "@/lib/menu";

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-slate-900 text-white">
      <div className="p-4">
        <h1 className="text-xl font-bold">CMS Platform</h1>
      </div>
      <nav className="mt-4">
        {adminMenu.map((item) => (
          <div key={item.title}>
            <Link
              href={item.url}
              className={cn(
                "flex items-center gap-3 px-4 py-2 text-sm",
                pathname === item.url
                  ? "bg-slate-800 text-white"
                  : "text-gray-400 hover:bg-slate-800 hover:text-white",
              )}
            >
              <item.icon className="h-4 w-4" />
              {item.title}
            </Link>
            {item.children && (
              <div className="ml-8 mt-1">
                {item.children.map((child) => (
                  <Link
                    key={child.title}
                    href={child.url}
                    className={cn(
                      "block px-4 py-2 text-sm",
                      pathname === child.url
                        ? "text-white"
                        : "text-gray-400 hover:text-white",
                    )}
                  >
                    {child.title}
                  </Link>
                ))}
              </div>
            )}
          </div>
        ))}
      </nav>
    </aside>
  );
}
```

### Página de Módulos

```tsx
// apps/web/app/(dashboard)/modules/page.tsx
"use client";

import { useQuery } from "@tanstack/react-query";
import { api } from "@/lib/api";
import { ModuleCard } from "@/components/admin/module-card";
import { Button } from "@/components/ui/button";

export default function ModulesPage() {
  const { data: modules, isLoading } = useQuery({
    queryKey: ["modules"],
    queryFn: () => api.get("/modules").then((res) => res.data),
  });

  if (isLoading) {
    return <div>Cargando módulos...</div>;
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Módulos</h1>
          <p className="text-gray-500">
            Activa o desactiva funcionalidades para tu sitio
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {modules?.map((module) => (
          <ModuleCard
            key={module.slug}
            module={module}
            onToggle={(isActive) => {
              // Handle toggle
            }}
          />
        ))}
      </div>
    </div>
  );
}
```

```tsx
// apps/web/components/admin/module-card.tsx
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import { FileText, ShoppingCart, Package, BarChart3, Lock } from "lucide-react";

const iconMap = {
  "file-text": FileText,
  "shopping-cart": ShoppingCart,
  package: Package,
  "bar-chart": BarChart3,
  lock: Lock,
};

interface ModuleCardProps {
  module: {
    slug: string;
    name: string;
    description: string;
    icon: string;
    version: string;
    is_active: boolean;
    is_system: boolean;
  };
  onToggle: (isActive: boolean) => void;
}

export function ModuleCard({ module, onToggle }: ModuleCardProps) {
  const Icon = iconMap[module.icon] || Package;

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="flex items-center gap-2">
          <Icon className="h-5 w-5" />
          {module.name}
        </CardTitle>
        {module.is_system && <Badge variant="secondary">Sistema</Badge>}
      </CardHeader>
      <CardContent>
        <p className="text-sm text-gray-500 mb-4">{module.description}</p>
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-400">v{module.version}</span>
          <div className="flex items-center gap-2">
            <span className="text-sm">
              {module.is_active ? "Activo" : "Inactivo"}
            </span>
            <Switch
              checked={module.is_active}
              onCheckedChange={onToggle}
              disabled={module.is_system}
            />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
```

---

## Plan de Desarrollo

### Semanas 1-2: Setup y Core

```
□ Configurar monorepo con Turborepo
□ Setup Docker + Docker Compose
□ Crear estructura de paquetes Python
□ Configurar PostgreSQL + Alembic
□ Implementar modelos base (Base, Timestamp, SoftDelete)
□ Implementar modelos core (User, Site, Module, SiteModule)
□ Sistema de migraciones
□ CRUD de usuarios con auth JWT
□ CRUD de sitios
□ Sistema de módulos básico (registro)
□ Tests unitarios de core
```

### Semanas 3-4: Sistema de Módulos

```
□ Implementar ModuleRegistry
□ Crear PluginBase class
□ Sistema de activación/desactivación
□ Hooks de ciclo de vida
□ Middleware de sitio (site resolver)
□ Admin menu dinámico
□ API de gestión de módulos
□ Tests de sistema de módulos
```

### Semanas 5-6: Módulo Blog

```
□ Modelos (Post, Category, Tag)
□ CRUD completo de posts
□ CRUD de categorías y tags
□ Editor WYSIWYG (Tiptap)
□ Preview de posts
□ API pública de blog
□ Tests del módulo
```

### Semanas 7-8: Frontend Admin Base

```
□ Setup Next.js
□ Configurar shadcn/ui
□ Layout principal (sidebar + header)
□ Dashboard
□ Página de sitios
□ Página de módulos
□ Página de usuarios
□ Rutas dinámicas de módulos
```

### Semanas 9-10: Módulo Store

```
□ Modelos (Product, Order, OrderItem, Cart)
□ CRUD de productos
□ Variantes de productos
□ Carrito de compras
□ Checkout flow
□ Gestión de pedidos
□ Estados de pedido
□ API del store
```

### Semanas 11-12: Módulo Inventario

```
□ Modelos (Stock, Warehouse)
□ Tracking de stock
□ Alertas de stock bajo
□ Ajustes de inventario
□ Reportes básicos
□ Integración con Store
```

### Semanas 13-14: Módulo Analytics

```
□ Modelo de eventos
□ Tracking de pageviews
□ Dashboard de métricas
□ Reportes
□ Integración con frontend
```

### Semanas 15-16: Polish y Deploy

```
□ Testing completo
□ Documentación de API
□ UI/UX refinamiento
□ Performance optimization
□ SEO optimization
□ Setup de producción
□ Deploy
```

---

## Setup Inicial

### Requisitos

- Node.js 20+
- Python 3.11+
- pnpm
- Docker Desktop
- PostgreSQL (vía Docker)
- Redis (vía Docker)

### Estructura de Archivos de Configuración

```yaml
# docker-compose.yml
version: "3.8"

services:
  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: cms
      POSTGRES_PASSWORD: cms_dev_password
      POSTGRES_DB: cms_dev
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  api:
    build:
      context: .
      dockerfile: docker/api.Dockerfile
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql+asyncpg://cms:cms_dev_password@postgres:5432/cms_dev
      REDIS_URL: redis://redis:6379
      JWT_SECRET: dev-secret-change-in-production
    depends_on:
      - postgres
      - redis
    volumes:
      - ./apps/api:/app/apps/api
      - ./packages:/app/packages

  web:
    build:
      context: .
      dockerfile: docker/web.Dockerfile
    ports:
      - "3000:3000"
    environment:
      API_URL: http://api:8000
    depends_on:
      - api
    volumes:
      - ./apps/web:/app/apps/web
      - ./packages/ui:/app/packages/ui

volumes:
  postgres_data:
  redis_data:
```

```toml
# pyproject.toml (apps/api)
[project]
name = "cms-api"
version = "0.1.0"
requires-python = ">=3.11"

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.109.0"
uvicorn = { extras = ["standard"], version = "^0.27.0" }
sqlalchemy = { extras = ["asyncio"], version = "^2.0.25" }
asyncpg = "^0.29.0"
alembic = "^1.13.1"
pydantic = "^2.5.3"
pydantic-settings = "^2.1.0"
python-jose = { extras = ["cryptography"], version = "^3.3.0" }
passlib = { extras = ["bcrypt"], version = "^1.7.4" }
python-multipart = "^0.0.6"
redis = "^5.0.1"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.4"
pytest-asyncio = "^0.23.3"
httpx = "^0.26.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

```json
// package.json (raíz)
{
  "name": "cms-platform",
  "private": true,
  "scripts": {
    "dev": "turbo dev",
    "build": "turbo build",
    "lint": "turbo lint",
    "test": "turbo test",
    "db:migrate": "cd apps/api && alembic upgrade head",
    "db:seed": "cd apps/api && python -m seed"
  },
  "devDependencies": {
    "turbo": "^2.0.0",
    "typescript": "^5.3.3"
  }
}
```

```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": ["**/.env.*local"],
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": [".next/**", "!.next/cache/**"]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {},
    "test": {}
  }
}
```

---

## Próximos Pasos

1. **Clonar este repositorio y setup inicial**
2. **Crear estructura de carpetas**
3. **Configurar Docker Compose**
4. **Implementar modelos core**
5. **Sistema de autenticación**
6. **Sistema de módulos**
7. **API REST base**
8. **Frontend admin**
9. **Módulos funcionales**

---

## Recursos

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
- [Next.js 14](https://nextjs.org/docs)
- [shadcn/ui](https://ui.shadcn.com)
- [Turborepo](https://turbo.build/repo)

---

_Documento creado: 2026-03-27_
_Versión: 1.0.0_
