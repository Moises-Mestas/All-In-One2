import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import Sidebar from "../../components/sidebar/sidebar";
import { authService, sitesService } from "../../services";
import "../sitioWeb/sitioWeb.css";

function Plantillas() {
  const navigate = useNavigate();
  // 👇 CORRECCIÓN 1: Eliminamos el estado 'user' que no se utilizaba
  const [templates, setTemplates] = useState<any[]>([]); 
  const [loading, setLoading] = useState(true);
  const [newTemplate, setNewTemplate] = useState({ name: "", slug: "" });
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
      // Validamos que el token funcione, pero no guardamos el resultado porque no se usa en la UI
      await authService.getMe();
      
      const allSites = await sitesService.getAll();
      setTemplates(allSites.filter((s: any) => s.is_template === true));
      
    } catch (err) {
      console.error("Error loading data:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTemplate = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setCreating(true);

    try {
      const payload = {
        name: newTemplate.name,
        slug: newTemplate.slug,
        is_template: true 
      };  

      const created = await sitesService.create(payload);
      setTemplates([...templates, created]);
      setNewTemplate({ name: "", slug: "" });
      alert("¡Plantilla creada! Ya puedes diseñarla en el editor.");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Error al crear plantilla");
    } finally {
      setCreating(false);
    }
  };

  const handleDeleteTemplate = async (id: number) => {
    if (!confirm("¿Eliminar definitivamente esta plantilla maestra?")) return;
    try {
      await sitesService.delete(id); 
      setTemplates(templates.filter((t) => t.id !== id));
    } catch (err) {
      console.error("Error deleting template:", err);
    }
  };

  const generateSlug = (name: string) => {
    // 👇 CORRECCIÓN 3: Usamos replaceAll en lugar de replace
    return name.toLowerCase().replaceAll(/[^a-z0-9]+/g, "-").replaceAll(/(^-|-$)/g, "");
  };

  if (loading) return <div className="loading">Cargando Gestor de Plantillas...</div>;

  return (
    <div className="sitioWeb-container">
      <Sidebar />
      <div className="main-content">
        <div className="sitioWeb-header">
          <div>
            <h1>Gestor de Plantillas</h1>
            <p className="user-email">Administra los modelos base para tus futuros sitios web</p>
          </div>
        </div>

        <div className="create-site-form">
          <h3>+ Nueva Plantilla Maestra en Blanco</h3>
          {error && <div className="error-message">{error}</div>}
          <form className="form-inline" onSubmit={handleCreateTemplate}>
            <div className="form-group">
              {/* 👇 CORRECCIÓN 2: Asociamos el label al input mediante htmlFor e id */}
              <label htmlFor="templateName">Nombre</label>
              <input 
                id="templateName"
                type="text" 
                value={newTemplate.name} 
                onChange={(e) => setNewTemplate({ name: e.target.value, slug: generateSlug(e.target.value) })} 
                placeholder="Ej. E-commerce Básico" 
                required 
              />
            </div>
            <div className="form-group">
              {/* 👇 CORRECCIÓN 2: Asociamos el label al input mediante htmlFor e id */}
              <label htmlFor="templateSlug">Slug (identificador)</label>
              <input 
                id="templateSlug"
                type="text" 
                value={newTemplate.slug} 
                onChange={(e) => setNewTemplate({ ...newTemplate, slug: generateSlug(e.target.value) })} 
                placeholder="ecommerce-basico" 
                required 
              />
            </div>
            <button type="submit" className="btn-primary" disabled={creating}>
              {creating ? "Creando..." : "Crear Plantilla"}
            </button>
          </form>
        </div>

        <div className="sites-section">
          <h2>Tus Diseños ({templates.length})</h2>
          <div className="sites-grid">
            {templates.map((template) => (
              <div key={template.id} className="site-card" style={{ borderLeft: "5px solid #2ecc71" }}>
                <div className="site-info" style={{ marginBottom: "20px" }}>
                  <h3>📄 {template.name}</h3>
                  <span className="site-slug">{template.slug}</span>
                </div>
                <div className="site-actions" style={{ display: "flex", gap: "10px", justifyContent: "flex-end" }}>
                  <button className="btn-icon" style={{ background: "#f39c12", color: "white" }} title="Editar Diseño Maestro" onClick={() => navigate(`/webEditor/${template.id}?isTemplate=true`)}>✏️</button>
                  <button className="btn-icon btn-danger" title="Eliminar Plantilla" onClick={() => handleDeleteTemplate(template.id)}>🗑</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
export default Plantillas;