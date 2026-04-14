import pytest
import time
from packages.modules.store.services import StoreService
from packages.modules.store.schemas import ProductoCreate,ProductoUpdate


def generate_slug():
    return f"site-{int(time.time() * 1000)}"


def generate_email():
    return f"user_{int(time.time() * 1000)}@mail.com"


async def create_site_and_login(client):
    email = generate_email()
    await client.post("/auth/register", json={"email": email, "password": "123456", "first_name": "Test", "last_name": "User"})
    login = await client.post("/auth/login", json={"email": email, "password": "123456"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    site_resp = await client.post("/sites", json={"name": "Test", "slug": generate_slug()}, headers=headers)
    return site_resp.json()["id"], headers


@pytest.mark.asyncio
async def test_crear_producto_sitio_no_existe(client):
    resp = await client.post(
        "/api/v1/sites/999999/tienda/productos",
        json={"nombre": "X", "slug": "x", "precio": 10, "stock": 1}
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_actualizar_producto_no_existe(client):
    site_id, headers = await create_site_and_login(client)

    resp = await client.put(
        f"/api/v1/sites/{site_id}/tienda/productos/99999",
        json={"nombre": "X"},
        headers=headers
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_eliminar_producto_no_existe(client):
    site_id, headers = await create_site_and_login(client)

    resp = await client.delete(
        f"/api/v1/sites/{site_id}/tienda/productos/99999",
        headers=headers
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_categoria_no_encontrada(client):
    site_id, headers = await create_site_and_login(client)

    resp = await client.get(
        f"/api/v1/sites/{site_id}/tienda/categorias/99999",
        headers=headers
    )
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_actualizar_estado_pedido_invalido(client):
    site_id, headers = await create_site_and_login(client)

    resp = await client.put(
        f"/api/v1/sites/{site_id}/tienda/pedidos/1/estado",
        json={"estado": "estado_fake"},
        headers=headers
    )
    assert resp.status_code in [400, 404]


@pytest.mark.asyncio
async def test_agregar_carrito_sin_usuario(client):
    site_id, headers = await create_site_and_login(client)

    resp = await client.post(
        f"/api/v1/sites/{site_id}/tienda/carrito/items",
        json={"producto_id": 1, "cantidad": 1},
        headers=headers
    )
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_checkout_error_validacion(client):
    site_id, headers = await create_site_and_login(client)

    resp = await client.post(
        f"/api/v1/sites/{site_id}/tienda/checkout",
        json={},  # vacío -> error
        headers=headers
    )
    assert resp.status_code in [400, 422]