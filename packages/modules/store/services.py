import sys
sys.path.insert(0, "/app")
sys.path.insert(0, "/app/packages")

import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import joinedload
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession
from packages.modules.store.models import (
    Categoria, Producto, Pedido, ItemPedido, Carrito, ItemCarrito,
    PedidoEstado, PedidoEstadoPago
)
from packages.modules.store.schemas import (
    CategoriaCreate, CategoriaUpdate, ProductoCreate, ProductoUpdate,
    ItemPedidoBase, CheckoutRequest
)

class StoreService:
    def __init__(self, db: AsyncSession, site_id: int):
        self.db = db
        self.site_id = site_id
    
    async def crear_categoria(self, data: CategoriaCreate) -> Categoria:
        categoria = Categoria(
            site_id=self.site_id,
            **data.model_dump()
        )
        self.db.add(categoria)
        await self.db.commit()
        await self.db.refresh(categoria)
        return categoria

    async def get_categoria(self, categoria_id: int) -> Categoria | None:
        result = await self.db.execute(
            select(Categoria).where(
                Categoria.id == categoria_id,
                Categoria.site_id == self.site_id
            )
        )
        return result.scalar_one_or_none()

    async def listar_categorias(self, solo_activas: bool = True) -> list[Categoria]:
        query = select(Categoria).where(Categoria.site_id == self.site_id)
        if solo_activas:
            query = query.where(Categoria.activa == True)
        query = query.order_by(Categoria.orden, Categoria.nombre)
        result = await self.db.execute(query)
        return list(result.scalars().all())

    async def actualizar_categoria(self, categoria_id: int, data: CategoriaUpdate) -> Categoria | None:
        categoria = await self.get_categoria(categoria_id)
        if not categoria:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(categoria, key, value)
        
        await self.db.commit()
        await self.db.refresh(categoria)
        return categoria

    async def eliminar_categoria(self, categoria_id: int) -> bool:
        categoria = await self.get_categoria(categoria_id)
        if not categoria:
            return False
        await self.db.delete(categoria)
        await self.db.commit()
        return True

    # ==================== PRODUCTOS ====================

    async def crear_producto(self, data: ProductoCreate) -> Producto:
        producto = Producto(
            site_id=self.site_id,
            **data.model_dump()
        )
        self.db.add(producto)
        await self.db.commit()
        await self.db.refresh(producto)
        return producto

    async def get_producto(self, producto_id: int) -> Producto | None:
        result = await self.db.execute(
            select(Producto).where(
                Producto.id == producto_id,
                Producto.site_id == self.site_id
            )
        )
        return result.scalar_one_or_none()

    async def listar_productos(
        self, 
        categoria_id: int | None = None,
        solo_activos: bool = True,
        featured: bool = False,
        page: int = 1,
        per_page: int = 20
    ) -> tuple[list[Producto], int]:
        query = select(Producto).where(Producto.site_id == self.site_id)
        
        if solo_activos:
            query = query.where(Producto.es_activo == True)
        if categoria_id:
            query = query.where(Producto.categoria_id == categoria_id)
        if featured:
            query = query.where(Producto.es_featured == True)
        
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        query = query.order_by(Producto.created_at.desc())
        query = query.offset((page - 1) * per_page).limit(per_page)
        
        result = await self.db.execute(query)
        return list(result.scalars().all()), total

    async def actualizar_producto(self, producto_id: int, data: ProductoUpdate) -> Producto | None:
        producto = await self.get_producto(producto_id)
        if not producto:
            return None
        
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(producto, key, value)
        
        await self.db.commit()
        await self.db.refresh(producto)
        return producto

    async def eliminar_producto(self, producto_id: int) -> bool:
        producto = await self.get_producto(producto_id)
        if not producto:
            return False
        await self.db.delete(producto)
        await self.db.commit()
        return True

    # ==================== PEDIDOS & CHECKOUT ====================

    def _generar_numero_pedido(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        short_uuid = str(uuid.uuid4())[:8].upper()
        return f"PED-{timestamp}-{short_uuid}"

    async def crear_pedido(self, data: CheckoutRequest, usuario_id: int | None = None) -> Pedido:
        query = select(Carrito).where(
            Carrito.site_id == self.site_id
        )
        if usuario_id:
            query = query.where(Carrito.usuario_id == usuario_id)
        
        result = await self.db.execute(query)
        carrito = result.scalar_one_or_none()
        
        items_carrito = []
        if carrito:
            result = await self.db.execute(
                select(ItemCarrito).where(ItemCarrito.carrito_id == carrito.id)
            )
            items_carrito = list(result.scalars().all())
        
        if not items_carrito:
            raise ValueError("El carrito está vacío")
        
        subtotal = Decimal('0.0')
        items_pedido = []
        
        # PROCESAMOS CADA ITEM Y AHORA SÍ DESCONTAMOS EL STOCK REAL
        for item in items_carrito:
            producto = await self.get_producto(item.producto_id)
            if not producto or not producto.es_activo:
                continue
            
            # Verificamos y descontamos stock real al momento de pagar
            if producto.stock is not None:
                if producto.stock < item.cantidad:
                    raise ValueError(f"Alguien nos ganó, ya no hay stock suficiente de: {producto.nombre}")
                producto.stock -= item.cantidad # <--- AHORA SE DESCUENTA EL STOCK AQUÍ
            
            item_total = producto.precio * item.cantidad
            subtotal += item_total
            
            items_pedido.append(ItemPedido(
                producto_id=producto.id,
                nombre_producto=producto.nombre,
                sku_producto=producto.sku,
                cantidad=item.cantidad,
                precio_unitario=producto.precio,
                total=item_total
            ))
        
        if not items_pedido:
            raise ValueError("No hay productos válidos en el carrito")
        
        impuesto = round(subtotal * Decimal('0.18'), 2)
        total = subtotal + impuesto
        
        pedido = Pedido(
            site_id=self.site_id,
            usuario_id=usuario_id,
            numero_pedido=self._generar_numero_pedido(),
            estado=PedidoEstado.PENDIENTE,
            estado_pago=PedidoEstadoPago.PENDIENTE,
            subtotal=subtotal,
            impuesto=impuesto,
            descuento=Decimal('0.0'),
            envio=Decimal('0.0'),
            total=total,
            nombre_cliente=data.nombre_cliente,
            email_cliente=data.email_cliente,
            telefono_cliente=data.telefono_cliente,
            direccion_envio=data.direccion_envio,
            ciudad_envio=data.ciudad_envio,
            pais_envio=data.pais_envio,
            codigo_postal=data.codigo_postal,
            metodo_pago=data.metodo_pago,
            notas=data.notas
        )
        
        self.db.add(pedido)
        await self.db.flush()
        
        for item in items_pedido:
            item.pedido_id = pedido.id
            self.db.add(item)
        
        if carrito:
            await self.db.execute(
                delete(ItemCarrito).where(ItemCarrito.carrito_id == carrito.id)
            )
        
        await self.db.commit()
        
        # MAGIA AQUÍ: Recargamos el pedido trayendo sus ítems de golpe para que FastAPI no crashee
        result_final = await self.db.execute(
            select(Pedido)
            .options(joinedload(Pedido.items))
            .where(Pedido.id == pedido.id)
        )
        pedido_completo = result_final.unique().scalar_one()
        
        return pedido_completo

    async def get_pedido(self, pedido_id: int) -> Pedido | None:
        result = await self.db.execute(
            select(Pedido).where(
                Pedido.id == pedido_id,
                Pedido.site_id == self.site_id
            )
        )
        return result.scalar_one_or_none()

    async def listar_pedidos(
        self,
        estado: str | None = None,
        page: int = 1,
        per_page: int = 20
    ) -> tuple[list[Pedido], int]:
        query = select(Pedido).where(Pedido.site_id == self.site_id)
        if estado:
            query = query.where(Pedido.estado == estado)
        
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        query = query.order_by(Pedido.created_at.desc())
        query = query.offset((page - 1) * per_page).limit(per_page)
        
        result = await self.db.execute(query)
        return list(result.scalars().all()), total

    async def actualizar_estado_pedido(self, pedido_id: int, nuevo_estado: str) -> Pedido | None:
        pedido = await self.get_pedido(pedido_id)
        if not pedido:
            return None
        try:
            pedido.estado = PedidoEstado(nuevo_estado)
        except ValueError:
            raise ValueError(f"Estado inválido: {nuevo_estado}")
        
        await self.db.commit()
        await self.db.refresh(pedido)
        return pedido

    # ==================== CARRITO ====================

    async def obtener_o_crear_carrito(self, usuario_id: int | None = None, session_id: str | None = None) -> Carrito:
        query = select(Carrito).where(Carrito.site_id == self.site_id)
        if usuario_id:
            query = query.where(Carrito.usuario_id == usuario_id)
        elif session_id:
            query = query.where(Carrito.session_id == session_id)
        
        result = await self.db.execute(query)
        carrito = result.scalar_one_or_none()
        
        if not carrito:
            carrito = Carrito(
                site_id=self.site_id,
                usuario_id=usuario_id,
                session_id=session_id
            )
            self.db.add(carrito)
            await self.db.commit()
            await self.db.refresh(carrito)
        
        return carrito

    async def agregar_al_carrito(self, producto_id: int, cantidad: int = 1, usuario_id: int | None = None, session_id: str | None = None):
        import uuid
        nuevo_session_id = None
        if not session_id:
            session_id = str(uuid.uuid4())
            nuevo_session_id = session_id
        
        producto = await self.get_producto(producto_id)
        if not producto or not producto.es_activo:
            raise ValueError("Producto no encontrado o no disponible")
        
        # SOLO VERIFICAMOS, YA NO DESCONTAMOS EL STOCK AQUÍ
        if producto.stock is not None and producto.stock < cantidad:
            raise ValueError("Stock insuficiente")
        
        carrito = await self.obtener_o_crear_carrito(usuario_id, session_id)
        
        result = await self.db.execute(
            select(ItemCarrito).where(
                ItemCarrito.carrito_id == carrito.id,
                ItemCarrito.producto_id == producto_id
            )
        )
        item_existente = result.scalar_one_or_none()
        
        if item_existente:
            nueva_cantidad = item_existente.cantidad + cantidad
            if producto.stock is not None and producto.stock < nueva_cantidad:
                raise ValueError("Stock insuficiente")
            item_existente.cantidad = nueva_cantidad
            await self.db.commit()
            await self.db.refresh(item_existente)
        else:
            # Quitamos la resta de stock aquí.
            item = ItemCarrito(
                carrito_id=carrito.id,
                producto_id=producto_id,
                cantidad=cantidad
            )
            self.db.add(item)
            await self.db.commit()
            await self.db.refresh(item)
            item_existente = item
        
        return item_existente, nuevo_session_id

    async def actualizar_cantidad_carrito(self, item_id: int, cantidad: int) -> ItemCarrito | None:
        result = await self.db.execute(
            select(ItemCarrito).where(ItemCarrito.id == item_id)
        )
        item = result.scalar_one_or_none()
        if not item:
            return None
        
        if cantidad <= 0:
            await self.db.delete(item)
            await self.db.commit()
            return None
        
        item.cantidad = cantidad
        await self.db.commit()
        await self.db.refresh(item)
        return item

    async def eliminar_del_carrito(self, item_id: int) -> bool:
        result = await self.db.execute(
            select(ItemCarrito).where(ItemCarrito.id == item_id)
        )
        item = result.scalar_one_or_none()
        if not item:
            return False
        
        await self.db.delete(item)
        await self.db.commit()
        return True

    async def obtener_carrito(self, usuario_id: int | None = None, session_id: str | None = None) -> Carrito | None:
        query = select(Carrito).where(Carrito.site_id == self.site_id)
        if usuario_id:
            query = query.where(Carrito.usuario_id == usuario_id)
        elif session_id:
            query = query.where(Carrito.session_id == session_id)
        
        result = await self.db.execute(query)
        return result.scalar_one_or_none()