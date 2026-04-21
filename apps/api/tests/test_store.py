"""
========================================
TEST SUITE: Módulo de Tienda (TC-019 a TC-021)
========================================
Módulo: packages.modules.store.routes
Funciones testadas:
- crear_categoria, crear_producto (TC-019)
- agregar_al_carrito (TC-020)
- Calculo de totales del carrito (TC-021)
"""

import pytest
import time
from decimal import Decimal


def generate_slug():
    """Genera un slug único para cada test"""
    return f"site-{int(time.time() * 1000)}"


def generate_email():
    """Genera un email único para cada test"""
    return f"user_{int(time.time() * 1000)}@mail.com"


async def create_site(client):
    """Helper: Crea un sitio y retorna su ID"""
    email = generate_email()

    await client.post("/auth/register", json={
        "email": email,
        "password": "123456",
        "first_name": "Test",
        "last_name": "User"
    })

    login = await client.post("/auth/login", json={
        "email": email,
        "password": "123456"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.post("/sites", json={
        "name": "Tienda Online",
        "slug": generate_slug(),
        "is_template": False
    }, headers=headers)

    return response.json()["id"], headers


# =========================================
# TC-019: Crear categoría y producto
# =========================================
@pytest.mark.asyncio
async def test_create_category_and_product(client):
    """TC-019: El tenant puede crear categoría y producto"""
    site_id, headers = await create_site(client)

    categoria_response = await client.post(
        f"/api/v1/sites/{site_id}/tienda/categorias",
        json={
            "nombre": "Ropa", 
            "slug": f"ropa-{int(time.time() * 1000)}",
            "descripcion": "Artículos de vestir"
        },
        headers=headers
    )

    assert categoria_response.status_code == 201
    categoria = categoria_response.json()
    categoria_id = categoria["id"]

    producto_response = await client.post(
        f"/api/v1/sites/{site_id}/tienda/productos",
        json={
            "nombre": "Polo React",
            "slug": f"polo-react-{int(time.time() * 1000)}",
            "descripcion": "Polo oficial de React",
            "precio": 50.00,
            "stock": 100,
            "sku": f"POLO-{int(time.time())}",
            "categoria_id": categoria_id,
            "es_activo": True
        },
        headers=headers
    )

    assert producto_response.status_code == 201
    producto = producto_response.json()
    assert producto["nombre"] == "Polo React"
    assert float(producto["precio"]) == 50.00
    assert producto["stock"] == 100
    assert producto["categoria_id"] == categoria_id


# =========================================
# TC-020: Agregar producto al carrito
# =========================================
@pytest.mark.asyncio
async def test_add_product_to_cart(client):
    """TC-020: El cliente puede agregar productos al carrito"""
    site_id, headers = await create_site(client)

    categoria_response = await client.post(
        f"/api/v1/sites/{site_id}/tienda/categorias",
        json={
            "nombre": "Accesorios",
            "slug": f"accesorios-{int(time.time() * 1000)}"
        },
        headers=headers
    )
    categoria_id = categoria_response.json()["id"]

    producto_response = await client.post(
        f"/api/v1/sites/{site_id}/tienda/productos",
        json={
            "nombre": "Gorra",
            "slug": f"gorra-{int(time.time() * 1000)}",
            "precio": 30.00,
            "stock": 50,
            "sku": f"GORRA-{int(time.time() * 1000)}",
            "categoria_id": categoria_id,
            "es_activo": True
        },
        headers=headers
    )
    producto_id = producto_response.json()["id"]

    usuario_id = int(time.time() * 1000)

    carrito_response = await client.post(
        f"/api/v1/sites/{site_id}/tienda/carrito/items",
        json={
            "producto_id": producto_id,
            "cantidad": 2,
            "usuario_id": usuario_id
        },
        headers=headers
    )

    assert carrito_response.status_code == 200
    item = carrito_response.json()
    assert item["cantidad"] == 2
    assert item["producto_id"] == producto_id


# =========================================
# TC-021: Cálculo de totales del carrito
# =========================================
@pytest.mark.asyncio
async def test_calculate_cart_totals(client):
    """TC-021: El sistema calcula correctamente los totales del carrito"""
    site_id, headers = await create_site(client)

    categoria_response = await client.post(
        f"/api/v1/sites/{site_id}/tienda/categorias",
        json={
            "nombre": "Test",
            "slug": f"test-cat-{int(time.time() * 1000)}"
        },
        headers=headers
    )
    categoria_id = categoria_response.json()["id"]

    producto1 = await client.post(
        f"/api/v1/sites/{site_id}/tienda/productos",
        json={
            "nombre": "Polo",
            "slug": f"polo-{int(time.time() * 1000)}",
            "precio": 50.00,
            "stock": 100,
            "sku": f"POLO-{int(time.time())}",
            "categoria_id": categoria_id,
            "es_activo": True
        },
        headers=headers
    )
    producto2 = await client.post(
        f"/api/v1/sites/{site_id}/tienda/productos",
        json={
            "nombre": "Gorra",
            "slug": f"gorra-{int(time.time() * 1000)}",
            "precio": 30.00,
            "stock": 50,
            "sku": f"GORRA-{int(time.time())}",
            "categoria_id": categoria_id,
            "es_activo": True
        },
        headers=headers
    )

    usuario_id = int(time.time() * 1000)

    await client.post(
        f"/api/v1/sites/{site_id}/tienda/carrito/items",
        json={"producto_id": producto1.json()["id"], "cantidad": 2, "usuario_id": usuario_id},
        headers=headers
    )
    await client.post(
        f"/api/v1/sites/{site_id}/tienda/carrito/items",
        json={"producto_id": producto2.json()["id"], "cantidad": 1, "usuario_id": usuario_id},
        headers=headers
    )

    carrito_response = await client.get(
        f"/api/v1/sites/{site_id}/tienda/carrito",
        params={"usuario_id": usuario_id},
        headers=headers
    )

    assert carrito_response.status_code == 200
    carrito = carrito_response.json()
    assert carrito["total"] == 130.00
    assert len(carrito["items"]) == 2
