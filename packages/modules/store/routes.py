import sys
sys.path.insert(0, "/app")
sys.path.insert(0, "/app/packages")

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List, Optional, Annotated

from app.db.database import get_db
from packages.core.models.site import Site
from packages.core.models.site_module import SiteModule
from packages.core.models.module import Module
from packages.modules.store.models import Carrito, ItemCarrito, Producto
from packages.modules.store.schemas import (
    CategoriaCreate, CategoriaUpdate, CategoriaResponse,
    ProductoCreate, ProductoUpdate, ProductoResponse, ProductoListado,
    PedidoListado, PedidoResponse, PedidoUpdateEstado,
    CarritoResponse, ItemCarritoCreate, ItemCarritoResponse,
    CheckoutRequest, CheckoutResponse
)
from packages.modules.store.services import StoreService

router = APIRouter(prefix="/api/v1/sites/{site_id}/tienda", tags=["tienda"])

# 👇 CONSTANTES PARA EVITAR TEXTOS DUPLICADOS (CODE SMELLS)
ERROR_SITIO_NO_ENCONTRADO = "Sitio no encontrado"
ERROR_PRODUCTO_NO_ENCONTRADO = "Producto no encontrado"
ERROR_CATEGORIA_NO_ENCONTRADA = "Categoría no encontrada"
ERROR_PEDIDO_NO_ENCONTRADO = "Pedido no encontrado"
ERROR_ITEM_NO_ENCONTRADO = "Item no encontrado"


async def get_site_tienda_module(db: AsyncSession, site_id: int) -> SiteModule | None:
    """Obtiene el site_module de tienda para un sitio"""
    result = await db.execute(
        select(Module).where(Module.slug == "tienda")
    )
    module = result.scalar_one_or_none()
    
    if not module:
        return None
    
    result = await db.execute(
        select(SiteModule).where(
            and_(
                SiteModule.site_id == site_id,
                SiteModule.module_id == module.id,
                SiteModule.is_active == True
            )
        )
    )
    return result.scalar_one_or_none()

# ==================== PRODUCTOS ====================

@router.get("/productos", response_model=dict, responses={404: {"description": ERROR_SITIO_NO_ENCONTRADO}})
async def listar_productos(
    site_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    categoria_id: Optional[int] = None,
    pagina: int = 1,
    por_pagina: int = 20,
    solo_activos: bool = True,
    featured: bool = False
):
    """Listar productos de la tienda"""
    result = await db.execute(select(Site).where(Site.id == site_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    
    service = StoreService(db, site_id)
    productos, total = await service.listar_productos(
        categoria_id=categoria_id,
        solo_activos=solo_activos,
        featured=featured,
        page=pagina,
        per_page=por_pagina
    )
    
    return {
        "success": True,
        "data": [ProductoListado.model_validate(p) for p in productos],
        "meta": {
            "total": total,
            "pagina": pagina,
            "por_pagina": por_pagina,
            "total_paginas": (total + por_pagina - 1) // por_pagina
        }
    }

@router.post("/productos", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED, responses={404: {"description": ERROR_SITIO_NO_ENCONTRADO}})
async def crear_producto(
    site_id: int,
    producto_data: ProductoCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Crear un nuevo producto"""
    result = await db.execute(select(Site).where(Site.id == site_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    
    service = StoreService(db, site_id)
    producto = await service.crear_producto(producto_data)
    
    await db.refresh(producto, ["categoria"])
    
    return producto

@router.get("/productos/{producto_id}", response_model=ProductoResponse, responses={404: {"description": "Sitio o Producto no encontrado"}})
async def obtener_producto(
    site_id: int,
    producto_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Obtener un producto por ID"""
    result = await db.execute(select(Site).where(Site.id == site_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    
    service = StoreService(db, site_id)
    producto = await service.get_producto(producto_id)
    
    if not producto:
        raise HTTPException(status_code=404, detail=ERROR_PRODUCTO_NO_ENCONTRADO)
    
    return producto

@router.put("/productos/{producto_id}", response_model=ProductoResponse, responses={404: {"description": "Sitio o Producto no encontrado"}})
async def actualizar_producto(
    site_id: int,
    producto_id: int,
    producto_data: ProductoUpdate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Actualizar un producto"""
    result = await db.execute(select(Site).where(Site.id == site_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    
    service = StoreService(db, site_id)
    producto = await service.actualizar_producto(producto_id, producto_data)
    
    if not producto:
        raise HTTPException(status_code=404, detail=ERROR_PRODUCTO_NO_ENCONTRADO)
    
    return producto

@router.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"description": "Sitio o Producto no encontrado"}})
async def eliminar_producto(
    site_id: int,
    producto_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Eliminar un producto"""
    result = await db.execute(select(Site).where(Site.id == site_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    
    service = StoreService(db, site_id)
    eliminado = await service.eliminar_producto(producto_id)
    
    if not eliminado:
        raise HTTPException(status_code=404, detail=ERROR_PRODUCTO_NO_ENCONTRADO)
    
    return None

# ==================== CATEGORÍAS ====================

@router.get("/categorias", response_model=dict, responses={404: {"description": ERROR_SITIO_NO_ENCONTRADO}})
async def listar_categorias(
    site_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    solo_activas: bool = True
):
    """Listar categorías de productos"""
    result = await db.execute(select(Site).where(Site.id == site_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    
    service = StoreService(db, site_id)
    categorias = await service.listar_categorias(solo_activas=solo_activas)
    
    return {
        "success": True,
        "data": [CategoriaResponse.model_validate(c) for c in categorias]
    }

@router.post("/categorias", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED, responses={404: {"description": ERROR_SITIO_NO_ENCONTRADO}})
async def crear_categoria(
    site_id: int,
    categoria_data: CategoriaCreate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Crear una nueva categoría"""
    result = await db.execute(select(Site).where(Site.id == site_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    
    service = StoreService(db, site_id)
    categoria = await service.crear_categoria(categoria_data)
    return categoria

@router.get("/categorias/{categoria_id}", response_model=CategoriaResponse, responses={404: {"description": "Sitio o Categoría no encontrada"}})
async def obtener_categoria(
    site_id: int,
    categoria_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Obtener una categoría por ID"""
    result = await db.execute(select(Site).where(Site.id == site_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    
    service = StoreService(db, site_id)
    categoria = await service.get_categoria(categoria_id)
    
    if not categoria:
        raise HTTPException(status_code=404, detail=ERROR_CATEGORIA_NO_ENCONTRADA)
    
    return categoria

@router.put("/categorias/{categoria_id}", response_model=CategoriaResponse, responses={404: {"description": "Sitio o Categoría no encontrada"}})
async def actualizar_categoria(
    site_id: int,
    categoria_id: int,
    categoria_data: CategoriaUpdate,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Actualizar una categoría"""
    result = await db.execute(select(Site).where(Site.id == site_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    
    service = StoreService(db, site_id)
    categoria = await service.actualizar_categoria(categoria_id, categoria_data)
    
    if not categoria:
        raise HTTPException(status_code=404, detail=ERROR_CATEGORIA_NO_ENCONTRADA)
    
    return categoria

@router.delete("/categorias/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"description": "Sitio o Categoría no encontrada"}})
async def eliminar_categoria(
    site_id: int,
    categoria_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Eliminar una categoría"""
    result = await db.execute(select(Site).where(Site.id == site_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    
    service = StoreService(db, site_id)
    eliminado = await service.eliminar_categoria(categoria_id)
    
    if not eliminado:
        raise HTTPException(status_code=404, detail=ERROR_CATEGORIA_NO_ENCONTRADA)
    
    return None

# ==================== PEDIDOS ====================

@router.get("/pedidos", response_model=dict, responses={404: {"description": ERROR_SITIO_NO_ENCONTRADO}})
async def listar_pedidos(
    site_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    estado: Optional[str] = None,
    pagina: int = 1,
    por_pagina: int = 20
):
    """Listar pedidos del sitio"""
    result = await db.execute(select(Site).where(Site.id == site_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    
    service = StoreService(db, site_id)
    pedidos, total = await service.listar_pedidos(
        estado=estado,
        page=pagina,
        per_page=por_pagina
    )
    
    return {
        "success": True,
        "data": [PedidoListado.model_validate(p) for p in pedidos],
        "meta": {
            "total": total,
            "pagina": pagina,
            "por_pagina": por_pagina,
            "total_paginas": (total + por_pagina - 1) // por_pagina
        }
    }

@router.get("/pedidos/{pedido_id}", response_model=PedidoResponse, responses={404: {"description": "Sitio o Pedido no encontrado"}})
async def obtener_pedido(
    site_id: int,
    pedido_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Obtener un pedido por ID"""
    result = await db.execute(select(Site).where(Site.id == site_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    
    service = StoreService(db, site_id)
    pedido = await service.get_pedido(pedido_id)
    
    if not pedido:
        raise HTTPException(status_code=404, detail=ERROR_PEDIDO_NO_ENCONTRADO)
    
    return pedido

@router.put("/pedidos/{pedido_id}/estado", response_model=PedidoResponse, responses={404: {"description": "Sitio o Pedido no encontrado"}, 400: {"description": "Estado inválido"}})
async def actualizar_estado_pedido(
    site_id: int,
    pedido_id: int,
    data: PedidoUpdateEstado,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Actualizar el estado de un pedido"""
    result = await db.execute(select(Site).where(Site.id == site_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    
    service = StoreService(db, site_id)
    
    try:
        pedido = await service.actualizar_estado_pedido(pedido_id, data.estado)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    if not pedido:
        raise HTTPException(status_code=404, detail=ERROR_PEDIDO_NO_ENCONTRADO)
    
    return pedido

# ==================== CARRITO ====================

@router.get("/carrito", response_model=CarritoResponse, responses={404: {"description": ERROR_SITIO_NO_ENCONTRADO}})
async def obtener_carrito(
    site_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    usuario_id: int = None
):
    """Obtener el carrito actual - usa usuario_id del query param"""
    try:
        result = await db.execute(select(Site).where(Site.id == site_id))
        if not result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
        
        if not usuario_id:
            return CarritoResponse(id=0, site_id=site_id, items=[], total=0)
        
        result = await db.execute(
            select(Carrito).where(
                Carrito.site_id == site_id,
                Carrito.usuario_id == usuario_id
            )
        )
        carrito = result.scalar_one_or_none()
        
        if not carrito:
            return CarritoResponse(id=0, site_id=site_id, items=[], total=0)
        
        result = await db.execute(
            select(ItemCarrito).where(ItemCarrito.carrito_id == carrito.id)
        )
        items = result.scalars().all()
        
        items_response = []
        total = 0
        for item in items:
            result = await db.execute(
                select(Producto).where(Producto.id == item.producto_id, Producto.es_activo == True)
            )
            producto = result.scalar_one_or_none()
            
            if producto:
                items_response.append(ItemCarritoResponse(
                    id=item.id,
                    producto_id=item.producto_id,
                    cantidad=item.cantidad,
                    producto=ProductoListado.model_validate(producto)
                ))
                total += producto.precio * item.cantidad
        
        return CarritoResponse(
            id=carrito.id,
            site_id=site_id,
            items=items_response,
            total=total
        )
    except Exception as e:
        print(f"Error en carrito: {e}")
        return CarritoResponse(id=0, site_id=site_id, items=[], total=0)

@router.post("/carrito/items", response_model=ItemCarritoResponse, responses={404: {"description": ERROR_SITIO_NO_ENCONTRADO}, 400: {"description": "Usuario no identificado o error de validación"}, 500: {"description": "Error interno"}})
async def agregar_al_carrito(
    site_id: int,
    item_data: ItemCarritoCreate,
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Agregar un producto al carrito - usa usuario_id del body"""
    try:
        result = await db.execute(select(Site).where(Site.id == site_id))
        if not result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
        
        usuario_id = item_data.usuario_id if hasattr(item_data, 'usuario_id') and item_data.usuario_id else None
        
        if not usuario_id:
            raise HTTPException(status_code=400, detail="Usuario no identificado")
        
        service = StoreService(db, site_id)
        
        try:
            item, nuevo_session_id = await service.agregar_al_carrito(
                producto_id=item_data.producto_id,
                cantidad=item_data.cantidad,
                usuario_id=usuario_id,
                session_id=None
            )
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        await db.refresh(item, ["producto"])
        
        return ItemCarritoResponse(
            id=item.id,
            producto_id=item.producto_id,
            cantidad=item.cantidad,
            producto=ProductoListado.model_validate(item.producto)
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al agregar al carrito: {e}")
        raise HTTPException(status_code=500, detail="Error interno")

@router.put("/carrito/items/{item_id}", response_model=ItemCarritoResponse, responses={404: {"description": "Sitio o Item no encontrado"}})
async def actualizar_cantidad_carrito(
    site_id: int,
    item_id: int,
    cantidad: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Actualizar la cantidad de un item en el carrito"""
    result = await db.execute(select(Site).where(Site.id == site_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    
    service = StoreService(db, site_id)
    item = await service.actualizar_cantidad_carrito(item_id, cantidad)
    
    if not item:
        raise HTTPException(status_code=404, detail=ERROR_ITEM_NO_ENCONTRADO)
    
    await db.refresh(item, ["producto"])
    
    return ItemCarritoResponse(
        id=item.id,
        producto_id=item.producto_id,
        cantidad=item.cantidad,
        producto=ProductoListado.model_validate(item.producto)
    )

@router.delete("/carrito/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT, responses={404: {"description": "Sitio o Item no encontrado"}})
async def eliminar_del_carrito(
    site_id: int,
    item_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Eliminar un item del carrito"""
    result = await db.execute(select(Site).where(Site.id == site_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    
    service = StoreService(db, site_id)
    eliminado = await service.eliminar_del_carrito(item_id)
    
    if not eliminado:
        raise HTTPException(status_code=404, detail=ERROR_ITEM_NO_ENCONTRADO)
    
    return None

@router.post("/checkout", response_model=CheckoutResponse, responses={404: {"description": ERROR_SITIO_NO_ENCONTRADO}, 400: {"description": "Error de validación"}, 500: {"description": "Error al procesar el pedido"}})
async def realizar_checkout(
    site_id: int,
    checkout_data: CheckoutRequest,
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    """Procesar el checkout y crear un pedido"""
    result = await db.execute(select(Site).where(Site.id == site_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail=ERROR_SITIO_NO_ENCONTRADO)
    
    session_id = request.cookies.get("carrito_session") or None
    
    usuario_id = checkout_data.usuario_id if hasattr(checkout_data, 'usuario_id') and checkout_data.usuario_id else None
    
    service = StoreService(db, site_id)
    
    try:
        pedido = await service.crear_pedido(checkout_data, usuario_id=usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Error en checkout: {e}")
        raise HTTPException(status_code=500, detail=f"Error al procesar el pedido: {str(e)}")
    
    return CheckoutResponse(
        pedido=PedidoResponse.model_validate(pedido),
        mensaje="Pedido creado exitosamente"
    )