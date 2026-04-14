import sys
sys.path.insert(0, "/app")
sys.path.insert(0, "/app/packages")

from sqlalchemy import String, Text, Integer, ForeignKey, Numeric, Boolean, Enum as SQLEnum, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from packages.core.models.base import BaseModel, TimestampMixin
import enum

# 👇 CONSTANTES PARA EVITAR TEXTOS DUPLICADOS (CODE SMELLS)
FK_SITES_ID = "sites.id"
FK_SITE_USERS_ID = "site_users.id"
ON_DELETE_SET_NULL = "SET NULL"
ON_DELETE_CASCADE = "CASCADE"


class Categoria(BaseModel, TimestampMixin):
    """Categoría de productos"""
    __tablename__ = "tienda_categorias"

    site_id: Mapped[int] = mapped_column(Integer, ForeignKey(FK_SITES_ID, ondelete=ON_DELETE_CASCADE), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("tienda_categorias.id", ondelete=ON_DELETE_SET_NULL), nullable=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    slug: Mapped[str] = mapped_column(String(100), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    imagen: Mapped[str | None] = mapped_column(String(500), nullable=True)
    orden: Mapped[int] = mapped_column(Integer, default=0)
    activa: Mapped[bool] = mapped_column(Boolean, default=True)

    parent: Mapped["Categoria | None"] = relationship("Categoria", remote_side="Categoria.id", back_populates="hijos")
    hijos: Mapped[list["Categoria"]] = relationship("Categoria", back_populates="parent")
    productos: Mapped[list["Producto"]] = relationship("Producto", back_populates="categoria")


class Producto(BaseModel, TimestampMixin):
    """Producto de la tienda"""
    __tablename__ = "tienda_productos"

    site_id: Mapped[int] = mapped_column(Integer, ForeignKey(FK_SITES_ID, ondelete=ON_DELETE_CASCADE), nullable=False)
    categoria_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("tienda_categorias.id", ondelete=ON_DELETE_SET_NULL), nullable=True)
    
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    sku: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    precio: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    precio_comparacion: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    costo: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    
    stock: Mapped[int] = mapped_column(Integer, default=0)
    stock_minimo: Mapped[int] = mapped_column(Integer, default=0)
    controlar_alertas: Mapped[bool] = mapped_column(Boolean, default=True)
    
    imagenes: Mapped[list] = mapped_column(JSON, default=list)
    peso: Mapped[float | None] = mapped_column(Numeric(10, 2), nullable=True)
    dimensiones: Mapped[dict | None] = mapped_column(JSON, default=None)
    
    es_activo: Mapped[bool] = mapped_column(Boolean, default=True)
    es_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    
    categoria: Mapped["Categoria"] = relationship("Categoria", back_populates="productos")
    items_pedido: Mapped[list["ItemPedido"]] = relationship("ItemPedido", back_populates="producto")
    items_carrito: Mapped[list["ItemCarrito"]] = relationship("ItemCarrito", back_populates="producto")


class PedidoEstado(str, enum.Enum):
    PENDIENTE = "pendiente"
    PROCESANDO = "procesando"
    ENVIADO = "enviado"
    ENTREGADO = "entregado"
    CANCELADO = "cancelado"
    REEMBOLSADO = "reembolsado"


class PedidoEstadoPago(str, enum.Enum):
    PENDIENTE = "pendiente"
    PAGADO = "pagado"
    FALLIDO = "fallido"
    REEMBOLSADO = "reembolsado"


class Pedido(BaseModel, TimestampMixin):
    """Pedido de un cliente"""
    __tablename__ = "tienda_pedidos"

    site_id: Mapped[int] = mapped_column(Integer, ForeignKey(FK_SITES_ID, ondelete=ON_DELETE_CASCADE), nullable=False)
    usuario_id: Mapped[int | None] = mapped_column(Integer, ForeignKey(FK_SITE_USERS_ID, ondelete=ON_DELETE_SET_NULL), nullable=True)
    
    numero_pedido: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    
    estado: Mapped[PedidoEstado] = mapped_column(SQLEnum(PedidoEstado), default=PedidoEstado.PENDIENTE)
    estado_pago: Mapped[PedidoEstadoPago] = mapped_column(SQLEnum(PedidoEstadoPago), default=PedidoEstadoPago.PENDIENTE)
    
    subtotal: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    impuesto: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    descuento: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    envio: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    total: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    
    nombre_cliente: Mapped[str] = mapped_column(String(200), nullable=False)
    email_cliente: Mapped[str] = mapped_column(String(255), nullable=False)
    telefono_cliente: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
    direccion_envio: Mapped[str | None] = mapped_column(Text, nullable=True)
    ciudad_envio: Mapped[str | None] = mapped_column(String(100), nullable=True)
    pais_envio: Mapped[str | None] = mapped_column(String(100), nullable=True)
    codigo_postal: Mapped[str | None] = mapped_column(String(20), nullable=True)
    
    metodo_pago: Mapped[str | None] = mapped_column(String(50), nullable=True)
    notas: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    items: Mapped[list["ItemPedido"]] = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")


class ItemPedido(BaseModel):
    """Ítem de un pedido"""
    __tablename__ = "tienda_items_pedido"

    pedido_id: Mapped[int] = mapped_column(Integer, ForeignKey("tienda_pedidos.id", ondelete=ON_DELETE_CASCADE), nullable=False)
    producto_id: Mapped[int] = mapped_column(Integer, ForeignKey("tienda_productos.id", ondelete=ON_DELETE_SET_NULL), nullable=True)
    
    nombre_producto: Mapped[str] = mapped_column(String(255), nullable=False)
    sku_producto: Mapped[str | None] = mapped_column(String(100), nullable=True)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)
    precio_unitario: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    total: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    pedido: Mapped["Pedido"] = relationship("Pedido", back_populates="items")
    producto: Mapped["Producto"] = relationship("Producto", back_populates="items_pedido")


class Carrito(BaseModel, TimestampMixin):
    """Carrito de compras"""
    __tablename__ = "tienda_carritos"

    site_id: Mapped[int] = mapped_column(Integer, ForeignKey(FK_SITES_ID, ondelete=ON_DELETE_CASCADE), nullable=False)
    usuario_id: Mapped[int | None] = mapped_column(Integer, ForeignKey(FK_SITE_USERS_ID, ondelete=ON_DELETE_SET_NULL), nullable=True)
    session_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    
    items: Mapped[list["ItemCarrito"]] = relationship("ItemCarrito", back_populates="carrito", cascade="all, delete-orphan")


class ItemCarrito(BaseModel):
    """Ítem en el carrito"""
    __tablename__ = "tienda_items_carrito"

    carrito_id: Mapped[int] = mapped_column(Integer, ForeignKey("tienda_carritos.id", ondelete=ON_DELETE_CASCADE), nullable=False)
    producto_id: Mapped[int] = mapped_column(Integer, ForeignKey("tienda_productos.id", ondelete=ON_DELETE_CASCADE), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, default=1)

    carrito: Mapped["Carrito"] = relationship("Carrito", back_populates="items")
    producto: Mapped["Producto"] = relationship("Producto", back_populates="items_carrito")