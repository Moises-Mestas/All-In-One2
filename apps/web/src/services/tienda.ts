import api from "./api";

const API_URL = "http://localhost:8000";

export interface Producto {
  id: number;
  nombre: string;
  slug: string;
  descripcion?: string;
  sku?: string;
  precio: number;
  precio_comparacion?: number;
  costo?: number;
  stock: number;
  stock_minimo: number;
  imagenes: string[];
  peso?: number;
  dimensiones?: any;
  es_activo: boolean;
  es_featured: boolean;
  categoria_id?: number;
  created_at?: string;
  updated_at?: string;
}

export interface Categoria {
  id: number;
  nombre: string;
  slug: string;
  descripcion?: string;
  imagen?: string;
  orden: number;
  activa: boolean;
  parent_id?: number;
}

export interface Pedido {
  id: number;
  numero_pedido: string;
  estado: string;
  estado_pago: string;
  nombre_cliente: string;
  email_cliente: string;
  telefono_cliente?: string;
  direccion_envio?: string;
  ciudad_envio?: string;
  pais_envio?: string;
  codigo_postal?: string;
  subtotal: number;
  impuesto: number;
  descuento: number;
  envio: number;
  total: number;
  metodo_pago?: string;
  notas?: string;
  created_at: string;
  items: PedidoItem[];
}

export interface PedidoItem {
  id: number;
  nombre_producto: string;
  sku_producto?: string;
  cantidad: number;
  precio_unitario: number;
  total: number;
}

export interface CarritoItem {
  id: number;
  producto_id: number;
  cantidad: number;
  producto: Producto;
}

export interface Carrito {
  id: number;
  site_id: number;
  items: CarritoItem[];
  total: number;
}

export interface DashboardStats {
  total_productos: number;
  productos_activos: number;
  total_pedidos: number;
  pedidos_pendientes: number;
  pedidos_entregados: number;
  ventas_mes: number;
}

class TiendaService {
  private baseUrl = API_URL;

  private getSiteId(): number {
    const siteIdMatch = window.location.pathname.match(/\/sitioWeb\/(\d+)/);
    if (siteIdMatch) return parseInt(siteIdMatch[1]);
    const stored = localStorage.getItem("currentSiteId");
    return stored ? parseInt(stored) : 1;
  }

  // ==================== PRODUCTOS ====================
  
  async getProductos(params?: {
    categoria_id?: number;
    solo_activos?: boolean;
    featured?: boolean;
    pagina?: number;
    por_pagina?: number;
  }): Promise<{ data: Producto[]; meta: any }> {
    const siteId = this.getSiteId();
    const queryParams = new URLSearchParams();
    if (params?.categoria_id) queryParams.append("categoria_id", params.categoria_id.toString());
    if (params?.solo_activos !== undefined) queryParams.append("solo_activos", params.solo_activos.toString());
    if (params?.featured) queryParams.append("featured", "true");
    if (params?.pagina) queryParams.append("pagina", params.pagina.toString());
    if (params?.por_pagina) queryParams.append("por_pagina", params.por_pagina.toString());
    
    const response = await api.get(`${this.baseUrl}/api/v1/sites/${siteId}/tienda/productos?${queryParams}`);
    return response.data;
  }

  async getProducto(id: number): Promise<Producto> {
    const siteId = this.getSiteId();
    const response = await api.get(`${this.baseUrl}/api/v1/sites/${siteId}/tienda/productos/${id}`);
    return response.data;
  }

  async createProducto(data: Partial<Producto>): Promise<Producto> {
    const siteId = this.getSiteId();
    const response = await api.post(`${this.baseUrl}/api/v1/sites/${siteId}/tienda/productos`, data);
    return response.data;
  }

  async updateProducto(id: number, data: Partial<Producto>): Promise<Producto> {
    const siteId = this.getSiteId();
    const response = await api.put(`${this.baseUrl}/api/v1/sites/${siteId}/tienda/productos/${id}`, data);
    return response.data;
  }

  async deleteProducto(id: number): Promise<void> {
    const siteId = this.getSiteId();
    await api.delete(`${this.baseUrl}/api/v1/sites/${siteId}/tienda/productos/${id}`);
  }

  async uploadImage(file: File): Promise<string> {
    const siteId = this.getSiteId();
    const formData = new FormData();
    formData.append("file", file);
    
    const response = await api.post(`/sites/${siteId}/upload-image`, formData, {
      headers: { "Content-Type": "multipart/form-data" }
    });
    return response.data.url;
  }

  // ==================== CATEGORÍAS ====================

  async getCategorias(solo_activas: boolean = true): Promise<Categoria[]> {
    const siteId = this.getSiteId();
    const response = await api.get(`${this.baseUrl}/api/v1/sites/${siteId}/tienda/categorias?solo_activas=${solo_activas}`);
    return response.data.data;
  }

  async getCategoria(id: number): Promise<Categoria> {
    const siteId = this.getSiteId();
    const response = await api.get(`${this.baseUrl}/api/v1/sites/${siteId}/tienda/categorias/${id}`);
    return response.data;
  }

  async createCategoria(data: Partial<Categoria>): Promise<Categoria> {
    const siteId = this.getSiteId();
    const response = await api.post(`${this.baseUrl}/api/v1/sites/${siteId}/tienda/categorias`, data);
    return response.data;
  }

  async updateCategoria(id: number, data: Partial<Categoria>): Promise<Categoria> {
    const siteId = this.getSiteId();
    const response = await api.put(`${this.baseUrl}/api/v1/sites/${siteId}/tienda/categorias/${id}`, data);
    return response.data;
  }

  async deleteCategoria(id: number): Promise<void> {
    const siteId = this.getSiteId();
    await api.delete(`${this.baseUrl}/api/v1/sites/${siteId}/tienda/categorias/${id}`);
  }

  // ==================== PEDIDOS ====================

  async getPedidos(params?: {
    estado?: string;
    pagina?: number;
    por_pagina?: number;
  }): Promise<{ data: Pedido[]; meta: any }> {
    const siteId = this.getSiteId();
    const queryParams = new URLSearchParams();
    if (params?.estado) queryParams.append("estado", params.estado);
    if (params?.pagina) queryParams.append("pagina", params.pagina.toString());
    if (params?.por_pagina) queryParams.append("por_pagina", params.por_pagina.toString());
    
    const response = await api.get(`${this.baseUrl}/api/v1/sites/${siteId}/tienda/pedidos?${queryParams}`);
    return response.data;
  }

  async getPedido(id: number): Promise<Pedido> {
    const siteId = this.getSiteId();
    const response = await api.get(`${this.baseUrl}/api/v1/sites/${siteId}/tienda/pedidos/${id}`);
    return response.data;
  }

  async actualizarEstadoPedido(id: number, estado: string): Promise<Pedido> {
    const siteId = this.getSiteId();
    const response = await api.put(`${this.baseUrl}/api/v1/sites/${siteId}/tienda/pedidos/${id}/estado`, { estado });
    return response.data;
  }

  // ==================== DASHBOARD ====================

  async getDashboardStats(): Promise<DashboardStats> {
    const siteId = this.getSiteId();
    
    const [productosRes, pedidosRes] = await Promise.all([
      api.get(`${this.baseUrl}/api/v1/sites/${siteId}/tienda/productos?solo_activos=false&por_pagina=1`),
      api.get(`${this.baseUrl}/api/v1/sites/${siteId}/tienda/pedidos?por_pagina=1`)
    ]);

    const productosData = productosRes.data;
    const pedidosData = pedidosRes.data;

    const pedidosPendientes = pedidosData.data.filter((p: Pedido) => p.estado === "pendiente");
    const pedidosEntregados = pedidosData.data.filter((p: Pedido) => p.estado === "entregado");
    
    const ventasMes = pedidosData.data
      .filter((p: Pedido) => p.estado === "entregado" || p.estado_pago === "pagado")
      .reduce((sum: number, p: Pedido) => sum + p.total, 0);

    return {
      total_productos: productosData.meta?.total || 0,
      productos_activos: productosData.data.filter((p: Producto) => p.es_activo).length,
      total_pedidos: pedidosData.meta?.total || 0,
      pedidos_pendientes: pedidosPendientes.length,
      pedidos_entregados: pedidosEntregados.length,
      ventas_mes: ventasMes
    };
  }

  // ==================== CARRITO (público) ====================

  async getCarrito(): Promise<Carrito> {
    const siteId = this.getSiteId();
    const response = await api.get(`${this.baseUrl}/api/v1/sites/${siteId}/tienda/carrito`);
    return response.data;
  }

  async agregarAlCarrito(productoId: number, cantidad: number = 1): Promise<CarritoItem> {
    const siteId = this.getSiteId();
    const response = await api.post(`${this.baseUrl}/api/v1/sites/${siteId}/tienda/carrito/items`, {
      producto_id: productoId,
      cantidad
    });
    return response.data;
  }

  async actualizarCantidad(itemId: number, cantidad: number): Promise<CarritoItem> {
    const siteId = this.getSiteId();
    const response = await api.put(`${this.baseUrl}/api/v1/sites/${siteId}/tienda/carrito/items/${itemId}?cantidad=${cantidad}`);
    return response.data;
  }

  async eliminarDelCarrito(itemId: number): Promise<void> {
    const siteId = this.getSiteId();
    await api.delete(`${this.baseUrl}/api/v1/sites/${siteId}/tienda/carrito/items/${itemId}`);
  }

  async checkout(data: {
    nombre_cliente: string;
    email_cliente: string;
    telefono_cliente?: string;
    direccion_envio?: string;
    ciudad_envio?: string;
    pais_envio?: string;
    codigo_postal?: string;
    metodo_pago: string;
    notas?: string;
  }) {
    const siteId = this.getSiteId();
    const response = await api.post(`${this.baseUrl}/api/v1/sites/${siteId}/tienda/checkout`, data);
    return response.data;
  }

  // Funciones locales del carrito (sin backend)
  getCarritoLocal(): { items: any[]; total: number } {
    const stored = localStorage.getItem("tienda_carrito");
    if (stored) {
      return JSON.parse(stored);
    }
    return { items: [], total: 0 };
  }

  agregarAlCarritoLocal(producto: Producto, cantidad: number = 1): void {
    let cart = this.getCarritoLocal();
    const existingIndex = cart.items.findIndex(item => item.producto.id === producto.id);
    
    if (existingIndex >= 0) {
      cart.items[existingIndex].cantidad += cantidad;
    } else {
      cart.items.push({ producto, cantidad });
    }
    
    cart.total = cart.items.reduce((sum, item) => sum + (item.producto.precio * item.cantidad), 0);
    localStorage.setItem("tienda_carrito", JSON.stringify(cart));
    this.actualizarUIContador();
  }

  eliminarDelCarritoLocal(productoId: number): void {
    let cart = this.getCarritoLocal();
    cart.items = cart.items.filter(item => item.producto.id !== productoId);
    cart.total = cart.items.reduce((sum, item) => sum + (item.producto.precio * item.cantidad), 0);
    localStorage.setItem("tienda_carrito", JSON.stringify(cart));
    this.actualizarUIContador();
  }

  limpiarCarritoLocal(): void {
    localStorage.removeItem("tienda_carrito");
    this.actualizarUIContador();
  }

  actualizarUIContador(): void {
    const cart = this.getCarritoLocal();
    const totalItems = cart.items.reduce((sum, item) => sum + item.cantidad, 0);
    
    document.querySelectorAll(".carrito-contador").forEach(el => {
      el.textContent = totalItems.toString();
    });
    
    document.querySelectorAll(".carrito-total").forEach(el => {
      el.textContent = `S/ ${cart.total.toFixed(2)}`;
    });
  }
}

export default new TiendaService();