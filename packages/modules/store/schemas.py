from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime


class CategoriaBase(BaseModel):
    nombre: str
    slug: str
    descripcion: Optional[str] = None
    imagen: Optional[str] = None
    orden: int = 0
    activa: bool = True


class CategoriaCreate(CategoriaBase):
    parent_id: Optional[int] = None


class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    slug: Optional[str] = None
    descripcion: Optional[str] = None
    imagen: Optional[str] = None
    orden: Optional[int] = None
    activa: Optional[bool] = None
    parent_id: Optional[int] = None


class CategoriaResponse(CategoriaBase):
    id: int
    parent_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CategoriaSimple(BaseModel):
    id: int
    nombre: str
    slug: str

    model_config = ConfigDict(from_attributes=True)


class ProductoBase(BaseModel):
    nombre: str
    slug: str
    descripcion: Optional[str] = None
    sku: Optional[str] = None
    precio: float
    precio_comparacion: Optional[float] = None
    costo: Optional[float] = None
    stock: int = 0
    stock_minimo: int = 0
    controlar_alertas: bool = True
    imagenes: list[Any] = []
    peso: Optional[float] = None
    dimensiones: Optional[dict[str, Any]] = None
    es_activo: bool = True
    es_featured: bool = False


class ProductoCreate(ProductoBase):
    categoria_id: Optional[int] = None


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    slug: Optional[str] = None
    descripcion: Optional[str] = None
    sku: Optional[str] = None
    precio: Optional[float] = None
    precio_comparacion: Optional[float] = None
    costo: Optional[float] = None
    stock: Optional[int] = None
    stock_minimo: Optional[int] = None
    controlar_alertas: Optional[bool] = None
    imagenes: Optional[list[Any]] = None
    peso: Optional[float] = None
    dimensiones: Optional[dict[str, Any]] = None
    es_activo: Optional[bool] = None
    es_featured: Optional[bool] = None
    categoria_id: Optional[int] = None


class ProductoResponse(ProductoBase):
    id: int
    categoria_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    categoria: Optional[CategoriaSimple] = None

    model_config = ConfigDict(from_attributes=True)


class ProductoListado(BaseModel):
    id: int
    nombre: str
    slug: str
    precio: float
    precio_comparacion: Optional[float] = None
    stock: int
    imagenes: list[Any]
    es_activo: bool
    es_featured: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ItemPedidoBase(BaseModel):
    producto_id: int
    nombre_producto: str
    sku_producto: Optional[str] = None
    cantidad: int
    precio_unitario: float


class ItemPedidoResponse(ItemPedidoBase):
    id: int
    total: float

    model_config = ConfigDict(from_attributes=True)


class PedidoBase(BaseModel):
    nombre_cliente: str
    email_cliente: str
    telefono_cliente: Optional[str] = None
    direccion_envio: Optional[str] = None
    ciudad_envio: Optional[str] = None
    pais_envio: Optional[str] = None
    codigo_postal: Optional[str] = None
    notas: Optional[str] = None


class PedidoCreate(PedidoBase):
    items: list[ItemPedidoBase]
    metodo_pago: str = "efectivo"


class PedidoUpdateEstado(BaseModel):
    estado: str


class PedidoResponse(PedidoBase):
    id: int
    site_id: int
    usuario_id: Optional[int] = None
    numero_pedido: str
    estado: str
    estado_pago: str
    subtotal: float
    impuesto: float
    descuento: float
    envio: float
    total: float
    metodo_pago: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    items: list[ItemPedidoResponse] = []

    model_config = ConfigDict(from_attributes=True)


class PedidoListado(BaseModel):
    id: int
    numero_pedido: str
    estado: str
    estado_pago: str
    nombre_cliente: str
    email_cliente: str
    total: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ItemCarritoBase(BaseModel):
    producto_id: int
    cantidad: int = 1


class ItemCarritoCreate(BaseModel):
    producto_id: int
    cantidad: int = 1
    usuario_id: int | None = None


class ItemCarritoResponse(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    producto: ProductoListado

    model_config = ConfigDict(from_attributes=True)


class CarritoResponse(BaseModel):
    id: int
    site_id: int
    items: list[ItemCarritoResponse] = []
    total: float = 0

    model_config = ConfigDict(from_attributes=True)


class CheckoutRequest(BaseModel):
    nombre_cliente: str
    email_cliente: str
    telefono_cliente: Optional[str] = None
    direccion_envio: Optional[str] = None
    ciudad_envio: Optional[str] = None
    pais_envio: Optional[str] = None
    codigo_postal: Optional[str] = None
    metodo_pago: str = "efectivo"
    notas: Optional[str] = None
    usuario_id: Optional[int] = None


class CheckoutResponse(BaseModel):
    pedido: PedidoResponse
    mensaje: str