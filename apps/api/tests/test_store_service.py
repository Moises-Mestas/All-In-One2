import pytest
from packages.modules.store.services import StoreService
from packages.modules.store.schemas import CategoriaCreate, CategoriaUpdate

@pytest.mark.asyncio
async def test_categoria_crud(db_session):
    service = StoreService(db_session, site_id=1)

    # Crear
    categoria = await service.crear_categoria(CategoriaCreate(
        nombre="Bebidas",
        slug="bebidas",
        descripcion="Bebidas frías",
        activa=True,
        orden=1
    ))
    assert categoria.id is not None

    # Obtener
    cat = await service.get_categoria(categoria.id)
    assert cat.nombre == "Bebidas"

    # Listar
    lista = await service.listar_categorias()
    assert len(lista) >= 1

    # Actualizar
    updated = await service.actualizar_categoria(
        categoria.id,
        CategoriaUpdate(nombre="Gaseosas")
    )
    assert updated.nombre == "Gaseosas"

    # Eliminar
    eliminado = await service.eliminar_categoria(categoria.id)
    assert eliminado is True


from packages.modules.store.schemas import ProductoCreate, ProductoUpdate
from decimal import Decimal

@pytest.mark.asyncio
async def test_producto_crud(db_session):
    service = StoreService(db_session, site_id=1)

    producto = await service.crear_producto(ProductoCreate(
        nombre="Coca Cola",
        slug="coca-cola",
        descripcion="Bebida",
        precio=Decimal("5.50"),
        stock=10,
        es_activo=True
    ))

    assert producto.id is not None

    prod = await service.get_producto(producto.id)
    assert prod.nombre == "Coca Cola"

    lista, total = await service.listar_productos()
    assert total >= 1

    updated = await service.actualizar_producto(
        producto.id,
        ProductoUpdate(nombre="Pepsi")
    )
    assert updated.nombre == "Pepsi"

    eliminado = await service.eliminar_producto(producto.id)
    assert eliminado is True    



@pytest.mark.asyncio
async def test_carrito_agregar_producto(db_session):
    service = StoreService(db_session, site_id=1)

    producto = await service.crear_producto(ProductoCreate(
        nombre="Laptop",
        slug="laptop",
        descripcion="Tech",
        precio=Decimal("1000"),
        stock=5,
        es_activo=True
    ))

    item, session_id = await service.agregar_al_carrito(
        producto_id=producto.id,
        cantidad=2
    )

    assert item.cantidad == 2
    assert session_id is not None    

@pytest.mark.asyncio
async def test_carrito_stock_insuficiente(db_session):
    service = StoreService(db_session, site_id=1)

    producto = await service.crear_producto(ProductoCreate(
        nombre="Mouse",
        slug="mouse",
        descripcion="Tech",
        precio=Decimal("50"),
        stock=1,
        es_activo=True
    ))

    with pytest.raises(ValueError):
        await service.agregar_al_carrito(
            producto_id=producto.id,
            cantidad=5
        )    


from packages.modules.store.schemas import CheckoutRequest

@pytest.mark.asyncio
async def test_crear_pedido(db_session):
    service = StoreService(db_session, site_id=1)

    producto = await service.crear_producto(ProductoCreate(
        nombre="Teclado",
        slug="teclado",
        descripcion="Tech",
        precio=Decimal("100"),
        stock=10,
        es_activo=True
    ))

    # Agregar al carrito
    item, session_id = await service.agregar_al_carrito(
        producto_id=producto.id,
        cantidad=2
    )

    pedido = await service.crear_pedido(CheckoutRequest(
        nombre_cliente="Ronald",
        email_cliente="test@mail.com",
        telefono_cliente="123456",
        direccion_envio="Puno",
        ciudad_envio="Puno",
        pais_envio="Peru",
        codigo_postal="21001",
        metodo_pago="efectivo",
        notas="ninguna"
    ))

    assert pedido.total > 0
    assert len(pedido.items) > 0        



@pytest.mark.asyncio
async def test_crear_pedido_carrito_vacio(db_session):
    service = StoreService(db_session, site_id=1)

    with pytest.raises(ValueError):
        await service.crear_pedido(CheckoutRequest(
            nombre_cliente="Test",
            email_cliente="test@mail.com",
            telefono_cliente="123",
            direccion_envio="X",
            ciudad_envio="X",
            pais_envio="X",
            codigo_postal="000",
            metodo_pago="efectivo",
            notas=""
        ))    


from packages.modules.store.schemas import PedidoUpdateEstado
import pytest

@pytest.mark.asyncio
async def test_listar_productos_paginacion(db_session):
    service = StoreService(db_session, site_id=1)
    
    for i in range(25):
        await service.crear_producto(ProductoCreate(
            nombre=f"Producto-{i}", slug=f"producto-{i}", descripcion="Test", precio=Decimal("10"), stock=10, es_activo=True
        ))
    
    lista, total = await service.listar_productos(page=1, per_page=10)
    assert len(lista) == 10
    assert total >= 25
    
    lista2, total2 = await service.listar_productos(page=2, per_page=10)
    assert len(lista2) >= 5


@pytest.mark.asyncio
async def test_get_producto_no_encontrado(db_session):
    service = StoreService(db_session, site_id=1)
    prod = await service.get_producto(99999)
    assert prod is None


@pytest.mark.asyncio
async def test_actualizar_producto_parcial(db_session):
    service = StoreService(db_session, site_id=1)
    
    prod = await service.crear_producto(ProductoCreate(
        nombre="Original", slug="original-test", descripcion="Test", precio=Decimal("10"), stock=10, es_activo=True
    ))
    
    updated = await service.actualizar_producto(prod.id, ProductoUpdate(precio=Decimal("20")))
    assert updated.precio == Decimal("20")
    assert updated.nombre == "Original"


@pytest.mark.asyncio
async def test_crear_pedido_con_usuario(db_session):
    import uuid
    service = StoreService(db_session, site_id=1)
    
    prod = await service.crear_producto(ProductoCreate(
        nombre="Test", slug="test-pedido-usuario", descripcion="Test", precio=Decimal("100"), stock=10, es_activo=True
    ))
    
    session_id = str(uuid.uuid4())
    item, _ = await service.agregar_al_carrito(producto_id=prod.id, cantidad=2, usuario_id=1, session_id=session_id)
    
    pedido = await service.crear_pedido(CheckoutRequest(
        nombre_cliente="Test", email_cliente="test@test.com", telefono_cliente="123",
        direccion_envio="X", ciudad_envio="X", pais_envio="X", codigo_postal="000",
        metodo_pago="efectivo", notas=""
    ), usuario_id=1)
    
    assert pedido.usuario_id == 1


@pytest.mark.asyncio
async def test_listar_pedidos_filtrados(db_session):
    service = StoreService(db_session, site_id=1)
    
    prod = await service.crear_producto(ProductoCreate(
        nombre="Test", slug="test-pedido-filtro", descripcion="Test", precio=Decimal("50"), stock=10, es_activo=True
    ))
    
    await service.agregar_al_carrito(producto_id=prod.id, cantidad=1)
    await service.crear_pedido(CheckoutRequest(
        nombre_cliente="A", email_cliente="a@test.com", telefono_cliente="1",
        direccion_envio="X", ciudad_envio="X", pais_envio="X", codigo_postal="000",
        metodo_pago="efectivo", notas=""
    ))
    
    lista, total = await service.listar_pedidos(estado="pendiente")
    assert total >= 1


@pytest.mark.asyncio
async def test_actualizar_estado_pedido(db_session):
    service = StoreService(db_session, site_id=1)
    
    prod = await service.crear_producto(ProductoCreate(
        nombre="Test", slug="test-estado-pedido", descripcion="Test", precio=Decimal("50"), stock=10, es_activo=True
    ))
    
    await service.agregar_al_carrito(producto_id=prod.id, cantidad=1)
    pedido = await service.crear_pedido(CheckoutRequest(
        nombre_cliente="A", email_cliente="a@test.com", telefono_cliente="1",
        direccion_envio="X", ciudad_envio="X", pais_envio="X", codigo_postal="000",
        metodo_pago="efectivo", notas=""
    ))
    
    updated = await service.actualizar_estado_pedido(pedido.id, "enviado")
    assert updated.estado.value == "enviado"


@pytest.mark.asyncio
async def test_carrito_actualizar_cantidad(db_session):
    service = StoreService(db_session, site_id=1)
    
    prod = await service.crear_producto(ProductoCreate(
        nombre="Test", slug="test-cantidad", descripcion="Test", precio=Decimal("10"), stock=10, es_activo=True
    ))
    
    item, _ = await service.agregar_al_carrito(producto_id=prod.id, cantidad=2)
    
    updated = await service.actualizar_cantidad_carrito(item.id, 5)
    assert updated.cantidad == 5
    
    removed = await service.actualizar_cantidad_carrito(item.id, 0)
    assert removed is None


@pytest.mark.asyncio
async def test_carrito_eliminar_item(db_session):
    service = StoreService(db_session, site_id=1)
    
    prod = await service.crear_producto(ProductoCreate(
        nombre="Test", slug="test-eliminar", descripcion="Test", precio=Decimal("10"), stock=10, es_activo=True
    ))
    
    item, _ = await service.agregar_al_carrito(producto_id=prod.id, cantidad=1)
    
    result = await service.eliminar_del_carrito(item.id)
    assert result is True
    
    result2 = await service.eliminar_del_carrito(99999)
    assert result2 is False


@pytest.mark.asyncio
async def test_obtener_carrito(db_session):
    service = StoreService(db_session, site_id=1)
    
    prod = await service.crear_producto(ProductoCreate(
        nombre="Test", slug="test-carrito", descripcion="Test", precio=Decimal("10"), stock=10, es_activo=True
    ))
    
    item, session_id = await service.agregar_al_carrito(producto_id=prod.id, cantidad=1)
    
    carrito = await service.obtener_carrito(session_id=session_id)
    assert carrito is not None


@pytest.mark.asyncio
async def test_listar_categorias_solo_activas(db_session):
    service = StoreService(db_session, site_id=1)
    
    await service.crear_categoria(CategoriaCreate(nombre="Activa", slug="activa", descripcion="A", activa=True, orden=1))
    await service.crear_categoria(CategoriaCreate(nombre="Inactiva", slug="inactiva", descripcion="I", activa=False, orden=2))
    
    activas = await service.listar_categorias(solo_activas=True)
    assert all(c.activa for c in activas)
    
    todas = await service.listar_categorias(solo_activas=False)
    assert len(todas) >= 2


@pytest.mark.asyncio
async def test_carrito_stock_insuficiente_al_agregar(db_session):
    service = StoreService(db_session, site_id=1)
    
    prod = await service.crear_producto(ProductoCreate(
        nombre="Test", slug="test-stock-carrito", descripcion="Test", precio=Decimal("10"), stock=2, es_activo=True
    ))
    
    with pytest.raises(ValueError, match="Stock insuficiente"):
        await service.agregar_al_carrito(producto_id=prod.id, cantidad=5)


@pytest.mark.asyncio
async def test_crear_categoria_sin_descripcion(db_session):
    service = StoreService(db_session, site_id=1)
    cat = await service.crear_categoria(CategoriaCreate(
        nombre="Nueva", slug="nueva-cat", activa=True, orden=5
    ))
    assert cat.id is not None
    assert cat.orden == 5


@pytest.mark.asyncio
async def test_crear_producto_sin_categoria(db_session):
    service = StoreService(db_session, site_id=1)
    prod = await service.crear_producto(ProductoCreate(
        nombre="Prod", slug="prod-sin-cat", precio=Decimal("10"), stock=5, es_activo=True
    ))
    assert prod.id is not None
    assert prod.categoria_id is None


@pytest.mark.asyncio
async def test_crear_producto_inactivo(db_session):
    service = StoreService(db_session, site_id=1)
    prod = await service.crear_producto(ProductoCreate(
        nombre="Inactivo", slug="inactivo", precio=Decimal("10"), stock=5, es_activo=False
    ))
    lista, total = await service.listar_productos(solo_activos=True)
    assert total == 0


@pytest.mark.asyncio
async def test_listar_productos_todos(db_session):
    service = StoreService(db_session, site_id=1)
    await service.crear_producto(ProductoCreate(
        nombre="Activo", slug="activo", precio=Decimal("10"), stock=5, es_activo=True
    ))
    await service.crear_producto(ProductoCreate(
        nombre="Inactivo2", slug="inactivo2", precio=Decimal("10"), stock=5, es_activo=False
    ))
    lista, total = await service.listar_productos(solo_activos=False)
    assert total >= 2


@pytest.mark.asyncio
async def test_listar_pedidos_vacio(db_session):
    service = StoreService(db_session, site_id=1)
    lista, total = await service.listar_pedidos()
    assert total == 0


@pytest.mark.asyncio
async def test_obtener_pedido_no_existe(db_session):
    service = StoreService(db_session, site_id=1)
    pedido = await service.get_pedido(99999)
    assert pedido is None    