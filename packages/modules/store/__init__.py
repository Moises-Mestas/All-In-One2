from packages.modules.store.module import Module


class TiendaModule(Module):
    name = "Tienda"
    slug = "tienda"
    version = "1.0.0"
    description = "Módulo de tienda virtual con productos, pedidos y carrito de compras"
    icon = "shopping-cart"
    admin_url = "/admin/tienda"
    is_system = False

    def get_models(self):
        from .models import Categoria, Producto, Pedido, ItemPedido, Carrito, ItemCarrito
        return [Categoria, Producto, Pedido, ItemPedido, Carrito, ItemCarrito]

    def get_schemas(self):
        from . import schemas
        return {
            "Categoria": schemas.CategoriaResponse,
            "Producto": schemas.ProductoResponse,
            "Pedido": schemas.PedidoResponse,
            "ItemPedido": schemas.ItemPedidoResponse,
            "Carrito": schemas.CarritoResponse,
        }

    def get_admin_menu(self):
        return [
            {
                "title": "Tienda",
                "url": self.admin_url,
                "icon": self.icon,
                "children": [
                    {"title": "Productos", "url": f"{self.admin_url}/productos"},
                    {"title": "Categorías", "url": f"{self.admin_url}/categorias"},
                    {"title": "Pedidos", "url": f"{self.admin_url}/pedidos"},
                    {"title": "Configuración", "url": f"{self.admin_url}/configuracion"},
                ]
            }
        ]


module = TiendaModule()