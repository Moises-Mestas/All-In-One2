import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import api from "../../../services/api";

export default function TiendaManager() {
  const { siteId } = useParams();
  const navigate = useNavigate();
  const [tab, setTab] = useState<"productos" | "pedidos">("productos");
  
  const [productos, setProductos] = useState<any[]>([]);
  const [loadingProductos, setLoadingProductos] = useState(true);
  const [formProducto, setFormProducto] = useState({
    nombre: "",
    slug: "",
    descripcion: "",
    sku: "",
    precio: 0,
    precio_comparacion: 0,
    stock: 0,
    es_activo: true,
    es_featured: false,
    imagenes: [] as string[]
  });

  const [pedidos, setPedidos] = useState<any[]>([]);
  const [loadingPedidos, setLoadingPedidos] = useState(true);
  const [subiendoImg, setSubiendoImg] = useState(false);

  useEffect(() => {
    if (tab === "productos") loadProductos();
    if (tab === "pedidos") loadPedidos();
  }, [tab, siteId]);

  const loadProductos = async () => {
    if (!siteId) return;
    try {
      const res = await api.get(`/api/v1/sites/${siteId}/tienda/productos?por_pagina=100`);
      setProductos(res.data.data);
    } catch (err) { console.error(err); }
    finally { setLoadingProductos(false); }
  };

  const loadPedidos = async () => {
    if (!siteId) return;
    try {
      const res = await api.get(`/api/v1/sites/${siteId}/tienda/pedidos?por_pagina=50`);
      setPedidos(res.data.data);
    } catch (err) { console.error(err); }
    finally { setLoadingPedidos(false); }
  };

  const guardarProducto = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!siteId) return;
    try {
      await api.post(`/api/v1/sites/${siteId}/tienda/productos`, formProducto);
      setFormProducto({ nombre: "", slug: "", descripcion: "", sku: "", precio: 0, precio_comparacion: 0, stock: 0, es_activo: true, es_featured: false, imagenes: [] });
      loadProductos();
      alert("Producto guardado!");
    } catch (err) { console.error(err); alert("Error al guardar"); }
  };

  const eliminarProducto = async (id: number) => {
    if (!siteId || !confirm("Eliminar producto?")) return;
    try {
      await api.delete(`/api/v1/sites/${siteId}/tienda/productos/${id}`);
      loadProductos();
    } catch (err) { console.error(err); }
  };

  const cambiarEstadoPedido = async (pedidoId: number, nuevoEstado: string) => {
    if (!siteId) return;
    try {
      await api.put(`/api/v1/sites/${siteId}/tienda/pedidos/${pedidoId}/estado`, { estado: nuevoEstado });
      loadPedidos();
    } catch (err) { console.error(err); alert("Error al cambiar estado"); }
  };

  const subirImagen = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file || !siteId) return;
    setSubiendoImg(true);
    try {
      const formData = new FormData();
      formData.append("file", file);
      const res = await api.post(`/sites/${siteId}/upload-image`, formData, { headers: { "Content-Type": "multipart/form-data" } });
      setFormProducto(prev => ({ ...prev, imagenes: [...prev.imagenes, res.data.url] }));
    } catch (err) { console.error(err); alert("Error al subir imagen"); }
    finally { setSubiendoImg(false); }
  };

  const generarSlug = (nombre: string) => nombre.toLowerCase().replace(/á/g,"a").replace(/é/g,"e").replace(/í/g,"i").replace(/ó/g,"o").replace(/ú/g,"u").replace(/[^a-z0-9]/g,"-").replace(/-+/g,"-").replace(/^-|-$/g,"");

  const inputStyle = { width: "100%", padding: "10px", background: "#2a2a2a", color: "#fff", border: "1px solid #444", borderRadius: "6px", boxSizing: "border-box" as const, marginBottom: "15px" };
  const labelStyle = { display: "block", marginBottom: "5px", fontSize: "14px", color: "#bbb", fontWeight: "bold" as const };

  return (
    <div style={{ padding: "30px", background: "#111", minHeight: "100vh", color: "white", fontFamily: "sans-serif" }}>
      <button onClick={() => navigate(-1)} style={{ padding: "8px 15px", background: "#333", color: "white", border: "none", borderRadius: "4px", marginBottom: "20px", cursor: "pointer" }}>Volver</button>
      
      <h1 style={{ borderBottom: "1px solid #333", paddingBottom: "15px" }}>Panel de Tienda</h1>
      
      <div style={{ marginBottom: "20px" }}>
        <button onClick={() => setTab("productos")} style={{ padding: "10px 20px", background: tab === "productos" ? "#3498db" : "#333", color: "white", border: "none", borderRadius: "4px", marginRight: "10px", cursor: "pointer" }}>Productos</button>
        <button onClick={() => setTab("pedidos")} style={{ padding: "10px 20px", background: tab === "pedidos" ? "#3498db" : "#333", color: "white", border: "none", borderRadius: "4px", cursor: "pointer" }}>Pedidos</button>
      </div>

      {tab === "productos" && (
        <form onSubmit={guardarProducto} style={{ display: "flex", gap: "30px", flexWrap: "wrap" }}>
          <div style={{ flex: "2", minWidth: "400px" }}>
            <div style={{ background: "#1e1e1e", padding: "25px", borderRadius: "8px", border: "1px solid #333", marginBottom: "20px" }}>
              <h3 style={{ marginTop: 0 }}>Productos Existentes</h3>
              {loadingProductos ? <p>Cargando...</p> : productos.length === 0 ? <p style={{ color: "#888" }}>No hay productos.</p> : (
                <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
                  {productos.map(p => (
                    <div key={p.id} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "15px", background: "#2a2a2a", borderRadius: "6px", border: "1px solid #444" }}>
                      <div>
                        <div style={{ fontWeight: "bold", fontSize: "16px" }}>{p.nombre}</div>
                        <div style={{ fontSize: "12px", color: p.es_activo ? "#4ade80" : "#ef4444" }}>
                          S/ {p.precio.toFixed(2)} - Stock: {p.stock}
                        </div>
                      </div>
                      <button type="button" onClick={() => eliminarProducto(p.id)} style={{ padding: "8px 12px", background: "#ef4444", color: "white", border: "none", borderRadius: "4px", cursor: "pointer" }}>Eliminar</button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>

          <div style={{ flex: "1", minWidth: "300px" }}>
            <div style={{ background: "#1e1e1e", padding: "25px", borderRadius: "8px", border: "1px solid #333" }}>
              <h3 style={{ marginTop: 0, color: "#3498db" }}>Nuevo Producto</h3>
              
              <label style={labelStyle} htmlFor="prod-nombre">Nombre *</label>
              <input id="prod-nombre" type="text" value={formProducto.nombre} onChange={(e) => setFormProducto({ ...formProducto, nombre: e.target.value, slug: generarSlug(e.target.value) })} style={{ ...inputStyle, fontWeight: "bold" }} required autoComplete="off" />
              
              <label style={labelStyle} htmlFor="prod-slug">Slug</label>
              <input id="prod-slug" type="text" value={formProducto.slug} onChange={(e) => setFormProducto({ ...formProducto, slug: e.target.value })} style={inputStyle} autoComplete="off" />
              
              <label style={labelStyle} htmlFor="prod-desc">Descripcion</label>
              <textarea id="prod-desc" value={formProducto.descripcion} onChange={(e) => setFormProducto({ ...formProducto, descripcion: e.target.value })} rows={3} style={{ ...inputStyle, resize: "vertical" }} />
              
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px" }}>
                <div>
                  <label style={labelStyle} htmlFor="prod-sku">SKU</label>
                  <input id="prod-sku" type="text" value={formProducto.sku} onChange={(e) => setFormProducto({ ...formProducto, sku: e.target.value })} style={inputStyle} autoComplete="off" />
                </div>
                <div>
                  <label style={labelStyle} htmlFor="prod-stock">Stock</label>
                  <input id="prod-stock" type="number" value={formProducto.stock} onChange={(e) => setFormProducto({ ...formProducto, stock: parseInt(e.target.value) || 0 })} style={inputStyle} />
                </div>
              </div>

              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "10px" }}>
                <div>
                  <label style={labelStyle} htmlFor="prod-precio">Precio *</label>
                  <input id="prod-precio" type="number" step="0.01" value={formProducto.precio} onChange={(e) => setFormProducto({ ...formProducto, precio: parseFloat(e.target.value) || 0 })} style={inputStyle} required />
                </div>
                <div>
                  <label style={labelStyle} htmlFor="prod-precio-ant">Precio Anterior</label>
                  <input id="prod-precio-ant" type="number" step="0.01" value={formProducto.precio_comparacion} onChange={(e) => setFormProducto({ ...formProducto, precio_comparacion: parseFloat(e.target.value) || 0 })} style={inputStyle} />
                </div>
              </div>

              <label style={labelStyle} htmlFor="prod-img">Imagen</label>
              <input id="prod-img" type="file" accept="image/*" onChange={subirImagen} disabled={subiendoImg} style={{ ...inputStyle, padding: "8px" }} autoComplete="off" />
              {subiendoImg && <p style={{ color: "#3498db", fontSize: "14px" }}>Subiendo...</p>}
              {formProducto.imagenes.length > 0 && (
                <div style={{ marginBottom: "15px" }}>
                  {formProducto.imagenes.map((url, i) => (
                    <img key={i} src={url} alt="" style={{ width: "80px", height: "80px", objectFit: "cover", borderRadius: "4px", marginRight: "5px" }} />
                  ))}
                </div>
              )}

              <div style={{ marginBottom: "15px" }}>
                <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer" }}>
                  <input type="checkbox" checked={formProducto.es_activo} onChange={(e) => setFormProducto({ ...formProducto, es_activo: e.target.checked })} />
                  <span>Activo</span>
                </label>
                <label style={{ display: "flex", alignItems: "center", gap: "8px", cursor: "pointer" }}>
                  <input type="checkbox" checked={formProducto.es_featured} onChange={(e) => setFormProducto({ ...formProducto, es_featured: e.target.checked })} />
                  <span>Destacado</span>
                </label>
              </div>

              <button type="submit" style={{ width: "100%", padding: "15px", background: "#3498db", color: "white", fontWeight: "bold", border: "none", borderRadius: "6px", cursor: "pointer", fontSize: "16px" }}>Guardar Producto</button>
            </div>
          </div>
        </form>
      )}

      {tab === "pedidos" && (
        <div style={{ background: "#1e1e1e", padding: "25px", borderRadius: "8px", border: "1px solid #333" }}>
          <h3 style={{ marginTop: 0 }}>Pedidos</h3>
          {loadingPedidos ? <p>Cargando...</p> : pedidos.length === 0 ? <p style={{ color: "#888" }}>No hay pedidos.</p> : (
            <div style={{ display: "flex", flexDirection: "column", gap: "15px" }}>
              {pedidos.map(pedido => (
                <div key={pedido.id} style={{ padding: "20px", background: "#2a2a2a", borderRadius: "6px", border: "1px solid #444" }}>
                  <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "10px" }}>
                    <div>
                      <div style={{ fontWeight: "bold", fontSize: "16px" }}>{pedido.numero_pedido}</div>
                      <div style={{ fontSize: "14px", color: "#888" }}>{pedido.nombre_cliente} - {pedido.email_cliente}</div>
                    </div>
                    <div style={{ textAlign: "right" }}>
                      <div style={{ fontWeight: "bold", fontSize: "18px", color: "#10b981" }}>S/ {pedido.total.toFixed(2)}</div>
                      <select value={pedido.estado} onChange={(e) => cambiarEstadoPedido(pedido.id, e.target.value)} style={{ marginTop: "5px", padding: "5px", background: "#333", color: "white", border: "1px solid #555", borderRadius: "4px" }}>
                        <option value="pendiente">Pendiente</option>
                        <option value="procesando">Procesando</option>
                        <option value="enviado">Enviado</option>
                        <option value="entregado">Entregado</option>
                        <option value="cancelado">Cancelado</option>
                      </select>
                    </div>
                  </div>
                  <div style={{ fontSize: "12px", color: "#666" }}>
                    Estado: <span style={{ color: pedido.estado === "entregado" ? "#10b981" : "#f59e0b" }}>{pedido.estado.toUpperCase()}</span> | 
                    Pago: <span style={{ color: pedido.estado_pago === "pagado" ? "#10b981" : "#f59e0b" }}>{pedido.estado_pago.toUpperCase()}</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}