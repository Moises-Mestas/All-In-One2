import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "../../components/sidebar/sidebar";
import { authService, sitesService } from "../../services";
import type { Site } from "../../types";
import "./sitioWeb.css";

function SitioWeb() {
  const navigate = useNavigate();
  const [user, setUser] = useState<any>(null);
  const [sites, setSites] = useState<Site[]>([]);
  const [templates, setTemplates] = useState<Site[]>([]);
  const [loading, setLoading] = useState(true);
  const [newSite, setNewSite] = useState({ name: "", slug: "", template_id: "" });
  const [error, setError] = useState("");
  const [creating, setCreating] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }
    loadData();
  }, [navigate]);

  const loadData = async () => {
    try {
      const userData = await authService.getMe();
      setUser(userData);
      
      const allSites = await sitesService.getAll();
      setSites(allSites.filter((s: any) => !s.is_template));
      setTemplates(allSites.filter((s: any) => s.is_template));
      
    } catch (err) {
      console.error("Error loading data:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateSite = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setCreating(true);

    try {
      // 🚀 Ahora el backend se encarga de copiar el diseño. 
      // Solo le enviamos el template_id.
      const created = await sitesService.create({
        name: newSite.name,
        slug: newSite.slug,
        is_template: false,
        // 👇 CORRECCIÓN 1: Condición positiva primero (si está vacío manda null, sino el id)
        template_id: newSite.template_id === "" ? null : newSite.template_id
      });

      setSites([...sites, created]);
      setNewSite({ name: "", slug: "", template_id: "" }); 
      alert("¡Sitio web creado exitosamente!");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Error al crear site");
    } finally {
      setCreating(false);
    }
  };

  const handleDeleteSite = async (id: number) => {
    if (!confirm("¿Estás seguro de eliminar este site?")) return;
    try {
      await sitesService.delete(id);
      setSites(sites.filter((s) => s.id !== id));
    } catch (err) {
      console.error("Error deleting site:", err);
    }
  };

  const generateSlug = (name: string) => {
    // 👇 CORRECCIÓN 2: Usar replaceAll
    return name.toLowerCase().replaceAll(/[^a-z0-9]+/g, "-").replaceAll(/(^-|-$)/g, "");
  };

  if (loading) return <div className="loading">Cargando Gestor de Sitios...</div>;

  return (
    <div className="sitioWeb-container">
      <Sidebar />
      <div className="main-content">
        <div className="sitioWeb-header">
          <div>
            <h1>Bienvenido, {user?.first_name}</h1>
            <p className="user-email">{user?.email}</p>
          </div>
        </div>

        <div className="create-site-form">
          <h3>+ Crear Nuevo Site</h3>
          {error && <div className="error-message">{error}</div>}
          <form className="form-inline" onSubmit={handleCreateSite} style={{ flexWrap: "wrap" }}>
            
            <div className="form-group">
              <label htmlFor="siteName">Nombre</label>
              <input 
                id="siteName"
                type="text" 
                value={newSite.name} 
                onChange={(e) => setNewSite({ ...newSite, name: e.target.value, slug: generateSlug(e.target.value) })} 
                placeholder="Mi Sitio Web" 
                required 
              />
            </div>

            <div className="form-group">
              <label htmlFor="siteSlug">Subdominio</label>
              <div className="input-group">
                <input 
                  id="siteSlug"
                  type="text" 
                  value={newSite.slug} 
                  onChange={(e) => setNewSite({ ...newSite, slug: generateSlug(e.target.value) })} 
                  placeholder="mi-sitio" 
                  required 
                />
                <span className="input-addon">.localtest.me</span>
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="siteTemplate">Usar Plantilla (Opcional)</label>
              <select 
                id="siteTemplate"
                value={newSite.template_id} 
                onChange={(e) => setNewSite({ ...newSite, template_id: e.target.value })} 
                style={{ padding: "10px", borderRadius: "4px", border: "1px solid #ddd", minWidth: "200px" }}
              >
                <option value="">Ninguna (Lienzo en blanco)</option>
                {templates.map(t => (
                  <option key={t.id} value={t.id}>{t.name} ({t.slug})</option>
                ))}
              </select>
            </div>

            <div className="form-group" style={{ display: "flex", alignItems: "flex-end" }}>
              <button type="submit" className="btn-primary" disabled={creating} style={{ height: "42px" }}>
                {creating ? "Creando..." : "Crear"}
              </button>
            </div>
            
          </form>
        </div>

        <div className="sites-section">
          <h2>Mis Sites ({sites.length})</h2>
          <div className="sites-grid">
            {sites.map((site) => (
              <div key={site.id} className="site-card">
                <div className="site-info">
                  <h3>{site.name}</h3>
                  <span className="site-slug">{site.slug}.localtest.me</span>
                </div>
                <div className="site-actions">
                  <button className="btn-icon btn-primary" title="Editar Diseño" onClick={() => navigate(`/webEditor/${site.id}`)}>✏️</button>
                  <a href={`http://localhost:8000/${site.slug}`} target="_blank" rel="noopener noreferrer" className="btn-icon" title="Ver sitio público">🌐</a>
                  <button className="btn-icon btn-danger" title="Eliminar" onClick={() => handleDeleteSite(site.id)}>🗑</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
export default SitioWeb;