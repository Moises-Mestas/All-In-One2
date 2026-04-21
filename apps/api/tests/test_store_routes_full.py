import pytest
import time
from decimal import Decimal
from packages.modules.store.services import StoreService
from packages.modules.store.schemas import (
    CategoriaCreate, CategoriaUpdate, ProductoCreate, ProductoUpdate, CheckoutRequest
)


def generate_slug():
    return f"site-{int(time.time() * 1000)}"


@pytest.mark.asyncio
async def test_listar_productos_featured(db_session):
    service = StoreService(db_session, site_id=1)
    await service.crear_producto(ProductoCreate(
        nombre="Featured", slug="featured", precio=Decimal("10"), stock=5, es_activo=True, es_featured=True
    ))
    await service.crear_producto(ProductoCreate(
        nombre="Normal", slug="normal", precio=Decimal("10"), stock=5, es_activo=True, es_featured=False
    ))
    lista, total = await service.listar_productos(featured=True)
    assert total >= 1


@pytest.mark.asyncio
async def test_listar_productos_por_pagina(db_session):
    service = StoreService(db_session, site_id=1)
    for i in range(15):
        await service.crear_producto(ProductoCreate(
            nombre=f"Prod{i}", slug=f"prod{i}", precio=Decimal("10"), stock=5, es_activo=True
        ))
    lista, total = await service.listar_productos(page=1, per_page=5)
    assert len(lista) == 5


@pytest.mark.asyncio
async def test_listar_productos_todos_incluyendo_inactivos(db_session):
    service = StoreService(db_session, site_id=1)
    await service.crear_producto(ProductoCreate(
        nombre="Activo", slug="activo", precio=Decimal("10"), stock=5, es_activo=True
    ))
    await service.crear_producto(ProductoCreate(
        nombre="Inactivo", slug="inactivo", precio=Decimal("10"), stock=5, es_activo=False
    ))
    lista, total = await service.listar_productos(solo_activos=False)
    assert total >= 2


@pytest.mark.asyncio
async def test_crear_producto_con_categoria(db_session):
    service = StoreService(db_session, site_id=1)
    cat = await service.crear_categoria(CategoriaCreate(
        nombre="Ropa", slug="ropa", descripcion="Ropa", activa=True, orden=1
    ))
    prod = await service.crear_producto(ProductoCreate(
        nombre="Camisa", slug="camisa", precio=Decimal("30"), stock=10, es_activo=True, categoria_id=cat.id
    ))
    assert prod.categoria_id == cat.id


@pytest.mark.asyncio
async def test_actualizar_producto_todos_campos(db_session):
    service = StoreService(db_session, site_id=1)
    prod = await service.crear_producto(ProductoCreate(
        nombre="Antes", slug="antes", precio=Decimal("10"), stock=5, es_activo=True
    ))
    updated = await service.actualizar_producto(
        prod.id,
        ProductoUpdate(nombre="Despues", precio=Decimal("50"), stock=20, es_activo=False)
    )
    assert updated.nombre == "Despues"
    assert float(updated.precio) == 50
    assert updated.stock == 20


@pytest.mark.asyncio
async def test_crear_pedido_sin_items(db_session):
    service = StoreService(db_session, site_id=1)
    with pytest.raises(ValueError, match="vacío"):
        await service.crear_pedido(CheckoutRequest(
            nombre_cliente="Test", email_cliente="test@test.com", telefono_cliente="123",
            direccion_envio="X", ciudad_envio="X", pais_envio="X", codigo_postal="000",
            metodo_pago="efectivo", notas=""
        ))


@pytest.mark.asyncio
async def test_carrito_crear_y_actualizar(db_session):
    service = StoreService(db_session, site_id=1)
    prod = await service.crear_producto(ProductoCreate(
        nombre="Test", slug="test-car", precio=Decimal("10"), stock=10, es_activo=True
    ))
    item, _ = await service.agregar_al_carrito(producto_id=prod.id, cantidad=2)
    updated = await service.actualizar_cantidad_carrito(item.id, 5)
    assert updated.cantidad == 5


@pytest.mark.asyncio
async def test_carrito_crear_y_eliminar(db_session):
    service = StoreService(db_session, site_id=1)
    prod = await service.crear_producto(ProductoCreate(
        nombre="Del", slug="del-car", precio=Decimal("10"), stock=10, es_activo=True
    ))
    item, _ = await service.agregar_al_carrito(producto_id=prod.id, cantidad=1)
    result = await service.eliminar_del_carrito(item.id)
    assert result is True


@pytest.mark.asyncio
async def test_crear_categoria_con_todos_campos(db_session):
    service = StoreService(db_session, site_id=1)
    cat = await service.crear_categoria(CategoriaCreate(
        nombre="Nueva", slug="nueva-cat", descripcion="Desc", activa=True, orden=5
    ))
    assert cat.nombre == "Nueva"
    assert cat.orden == 5


@pytest.mark.asyncio
async def test_crear_categoria_inactiva(db_session):
    service = StoreService(db_session, site_id=1)
    cat = await service.crear_categoria(CategoriaCreate(
        nombre="Inactiva", slug="inactiva", descripcion="Desc", activa=False, orden=1
    ))
    lista = await service.listar_categorias(solo_activas=True)
    assert len(lista) == 0


@pytest.mark.asyncio
async def test_listar_productos_por_categoria(db_session):
    service = StoreService(db_session, site_id=1)
    cat = await service.crear_categoria(CategoriaCreate(
        nombre="Cat", slug="cat", activa=True, orden=1
    ))
    await service.crear_producto(ProductoCreate(
        nombre="P1", slug="p1", precio=Decimal("10"), stock=5, es_activo=True, categoria_id=cat.id
    ))
    await service.crear_producto(ProductoCreate(
        nombre="P2", slug="p2", precio=Decimal("10"), stock=5, es_activo=True, categoria_id=cat.id
    ))
    lista, total = await service.listar_productos(categoria_id=cat.id)
    assert total == 2


@pytest.mark.asyncio
async def test_crear_pedido_sin_envio(db_session):
    service = StoreService(db_session, site_id=1)
    prod = await service.crear_producto(ProductoCreate(
        nombre="Test", slug="test-sin-envio", precio=Decimal("10"), stock=10, es_activo=True
    ))
    await service.agregar_al_carrito(producto_id=prod.id, cantidad=1)
    pedido = await service.crear_pedido(CheckoutRequest(
        nombre_cliente="Test", email_cliente="test@test.com", telefono_cliente="123",
        direccion_envio="X", ciudad_envio="X", pais_envio="X", codigo_postal="000",
        metodo_pago="efectivo", notas=""
    ))
    assert pedido.total > 0


@pytest.mark.asyncio
async def test_actualizar_categoria_todos_campos(db_session):
    service = StoreService(db_session, site_id=1)
    cat = await service.crear_categoria(CategoriaCreate(
        nombre="Old", slug="old-cat", activa=True, orden=1
    ))
    updated = await service.actualizar_categoria(
        cat.id,
        CategoriaUpdate(nombre="New", orden=10, activa=False)
    )
    assert updated.nombre == "New"
    assert updated.orden == 10


@pytest.mark.asyncio
async def test_actualizar_categoria_parcial(db_session):
    service = StoreService(db_session, site_id=1)
    cat = await service.crear_categoria(CategoriaCreate(
        nombre="Parcial", slug="parcial", activa=True, orden=1
    ))
    updated = await service.actualizar_categoria(cat.id, CategoriaUpdate(descripcion="New desc"))
    assert updated.descripcion == "New desc"


@pytest.mark.asyncio
async def test_actualizar_producto_con_sku(db_session):
    service = StoreService(db_session, site_id=1)
    prod = await service.crear_producto(ProductoCreate(
        nombre="Test", slug="test-sku", precio=Decimal("10"), stock=5, es_activo=True, sku="SKU123"
    ))
    assert prod.sku == "SKU123"


@pytest.mark.asyncio
async def test_carrito_sin_session_id(db_session):
    service = StoreService(db_session, site_id=1)
    prod = await service.crear_producto(ProductoCreate(
        nombre="Test", slug="test-no-session", precio=Decimal("10"), stock=10, es_activo=True
    ))
    item, session_id = await service.agregar_al_carrito(producto_id=prod.id, cantidad=1)
    assert session_id is not None


@pytest.mark.asyncio
async def test_obtener_o_crear_carrito_existente(db_session):
    service = StoreService(db_session, site_id=1)
    prod = await service.crear_producto(ProductoCreate(
        nombre="Test", slug="test-car-exists", precio=Decimal("10"), stock=10, es_activo=True
    ))
    item1, _ = await service.agregar_al_carrito(producto_id=prod.id, cantidad=1, usuario_id=1)
    item2, _ = await service.agregar_al_carrito(producto_id=prod.id, cantidad=2, usuario_id=1)
    assert item1.id == item2.id
    assert item2.cantidad == 3


@pytest.mark.asyncio
async def test_eliminar_producto_no_existe(db_session):
    service = StoreService(db_session, site_id=1)
    result = await service.eliminar_producto(99999)
    assert result is False


@pytest.mark.asyncio
async def test_eliminar_categoria_no_existe(db_session):
    service = StoreService(db_session, site_id=1)
    result = await service.eliminar_categoria(99999)
    assert result is False


@pytest.mark.asyncio
async def test_get_categoria_no_existe(db_session):
    service = StoreService(db_session, site_id=1)
    cat = await service.get_categoria(99999)
    assert cat is None


@pytest.mark.asyncio
async def test_listar_pedidos_por_estado(db_session):
    service = StoreService(db_session, site_id=1)
    prod = await service.crear_producto(ProductoCreate(
        nombre="Test", slug="test-estado", precio=Decimal("10"), stock=10, es_activo=True
    ))
    await service.agregar_al_carrito(producto_id=prod.id, cantidad=1)
    pedido = await service.crear_pedido(CheckoutRequest(
        nombre_cliente="A", email_cliente="a@test.com", telefono_cliente="1",
        direccion_envio="X", ciudad_envio="X", pais_envio="X", codigo_postal="000",
        metodo_pago="efectivo", notas=""
    ))
    await service.actualizar_estado_pedido(pedido.id, "enviado")
    lista, total = await service.listar_pedidos(estado="enviado")
    assert total >= 1