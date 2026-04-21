import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom"; // 👇 Importamos para navegar
import Sidebar from "../../components/sidebar/sidebar";
import { modulesService, siteModulesService, authModuleService, sitesService } from "../../services";
import "./modulos.css";

interface Module {
  id: number;
  name: string;
  slug: string;
  description: string;
  icon: string;
}

interface SiteModule {
  id: number;
  module_id: number;
  is_active: boolean;
  config: Record<string, any>;
}

interface Site {
  id: number;
  name: string;
  slug: string;
}

function Modulos() {
  const navigate = useNavigate(); // 👇 Inicializamos el navegador
  const [modules, setModules] = useState<Module[]>([]);
  const [siteModules, setSiteModules] = useState<SiteModule[]>([]);
  const [selectedSite, setSelectedSite] = useState<number | null>(null);
  const [sites, setSites] = useState<Site[]>([]);
  const [authConfig, setAuthConfig] = useState<{
    registration_fields: string[];
    custom_fields: Array<{ name: string; label: string }>;
    require_verification: boolean;
  }>({
    registration_fields: ["email", "password", "first_name", "last_name"],
    custom_fields: [],
    require_verification: false,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setError(null);
      const modulesRes = await modulesService.getAll();
      const sitesRes = await sitesService.getAll();
      
      setModules(modulesRes);
      setSites(sitesRes);
      
      if (sitesRes.length > 0) {
        setSelectedSite(sitesRes[0].id);
      }
    } catch (err: any) {
      console.error("Error loading data:", err);
      setError(err?.response?.data?.detail || "Error al cargar los datos");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedSite) {
      loadSiteModules(selectedSite);
    }
  }, [selectedSite]);

  const loadSiteModules = async (siteId: number) => {
    try {
      const res = await siteModulesService.getBySite(siteId);
      setSiteModules(res);
      
      const authSm = res.find((sm: SiteModule) => {
        const mod = modules.find((m: Module) => m.id === sm.module_id);
        return mod?.slug === "auth";
      });
      
      if (authSm?.config) {
        setAuthConfig({
          registration_fields: authSm.config.registration_fields || ["email", "password"],
          custom_fields: authSm.config.custom_fields || [],
          require_verification: authSm.config.require_verification || false,
        });
      } else {
        setAuthConfig(authModuleService.getDefaultConfig());
      }
    } catch (err) {
      console.error("Error loading site modules:", err);
    }
  };

  const toggleModule = async (module: Module) => {
    if (!selectedSite) return;
    
    const existing = siteModules.find(sm => sm.module_id === module.id);
    
    try {
      if (existing) {
        await siteModulesService.toggle(existing.id);
      } else {
        const config = module.slug === "auth" ? authConfig : {};
        await siteModulesService.create({
          site_id: selectedSite,
          module_id: module.id,
          is_active: true,
          config,
        });
      }
      
      loadSiteModules(selectedSite);
    } catch (err) {
      console.error("Error toggling module:", err);
      alert("Error al modificar el módulo");
    }
  };

  const isModuleActive = (moduleId: number): boolean => {
    const sm = siteModules.find(s => s.module_id === moduleId);
    return sm?.is_active || false;
  };

  const updateAuthField = (field: string, checked: boolean) => {
    setAuthConfig(prev => {
      const fields = checked 
        ? [...prev.registration_fields, field]
        : prev.registration_fields.filter(f => f !== field);
      return { ...prev, registration_fields: fields };
    });
  };

  const addCustomField = () => {
    const name = prompt("Nombre del campo (ej: empresa):");
    const label = prompt("Label del campo (ej: Empresa):");
    if (name && label) {
      setAuthConfig(prev => ({
        ...prev,
        custom_fields: [...prev.custom_fields, { name, label }],
      }));
    }
  };

  const removeCustomField = (name: string) => {
    setAuthConfig(prev => ({
      ...prev,
      custom_fields: prev.custom_fields.filter(f => f.name !== name),
    }));
  };

  const saveAuthConfig = async () => {
    if (!selectedSite) return;
    
    const authModule = modules.find(m => m.slug === "auth");
    if (!authModule) return;
    
    const existing = siteModules.find(sm => sm.module_id === authModule.id);
    
    try {
      if (existing) {
        await siteModulesService.update(existing.id, { 
          config: authConfig,
          is_active: true 
        });
      } else {
        await siteModulesService.create({
          site_id: selectedSite,
          module_id: authModule.id,
          is_active: true,
          config: authConfig,
        });
      }
      
      alert("Configuración guardada correctamente!");
      loadSiteModules(selectedSite);
    } catch (err) {
      console.error("Error saving config:", err);
      alert("Error al guardar la configuración");
    }
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <Sidebar />
        <div className="main-content">
          <div className="loading">Cargando...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-container">
      <Sidebar />
      <div className="main-content">
        <div className="modules-header">
          <h1>Módulos</h1>
          {sites.length > 0 && (
            <div className="site-selector">
              <label>Sitio:</label>
              <select 
                value={selectedSite || ""} 
                onChange={(e) => setSelectedSite(Number(e.target.value))}
              >
                {sites.map(site => (
                  <option key={site.id} value={site.id}>{site.name}</option>
                ))}
              </select>
            </div>
          )}
        </div>

        {error && (
          <div className="error-message">
            <p>{error}</p>
            <button onClick={loadData}>Reintentar</button>
          </div>
        )}

        {sites.length === 0 && !error && (
          <div className="empty-state">
            <p>No tienes sitios creados aún.</p>
          </div>
        )}

        {modules.length > 0 && (
          <div className="modules-grid">
            {modules.map(module => (
              <div 
                key={module.id} 
                className={`module-card ${isModuleActive(module.id) ? "active" : ""}`}
              >
                <div className="module-icon">{getModuleIcon(module.icon)}</div>
                <div className="module-info">
                  <h3>{module.name}</h3>
                  <p>{module.description || "Sin descripción"}</p>
                  
              
                </div>
                {module.slug === 'blog' && isModuleActive(module.id) && (
                <button 
                  onClick={() => navigate(`/sitioWeb/${selectedSite}/blog`)}
                  style={{ 
                    marginTop: '10px', 
                    padding: '8px', 
                    background: '#3498db', 
                    color: 'white', 
                    border: 'none', 
                    borderRadius: '4px', 
                    cursor: 'pointer',
                    fontWeight: 'bold' 
                  }}
                >
                  📝 Gestionar Artículos
                </button>
              )}
                <label className="switch">
                  <input
                    type="checkbox"
                    checked={isModuleActive(module.id)}
                    onChange={() => toggleModule(module)}
                    disabled={!selectedSite}
                  />
                  <span className="slider"></span>
                </label>
              </div>
            ))}
          </div>
        )}

        {/* Panel de Configuración de Auth (se mantiene igual) */}
        {isModuleActive(modules.find(m => m.slug === "auth")?.id || 0) && (
          <div className="auth-config-panel">
            <h2>Configuración de Auth</h2>
            
            <div className="config-section">
              <h3>Campos de Registro</h3>
              <p className="hint">Selecciona los campos que aparecerán en el formulario:</p>
              
              <div className="fields-grid">
                {authModuleService.AVAILABLE_FIELDS.map(field => (
                  <label key={field.value} className="field-checkbox">
                    <input
                      type="checkbox"
                      checked={authConfig.registration_fields.includes(field.value)}
                      onChange={(e) => updateAuthField(field.value, e.target.checked)}
                      disabled={field.required}
                    />
                    <span>{field.label}</span>
                    {field.required && <span className="required-badge">Requerido</span>}
                  </label>
                ))}
              </div>
            </div>

            <div className="config-section">
              <h3>Campos Personalizados</h3>
              <div className="custom-fields">
                {authConfig.custom_fields.map(field => (
                  <div key={field.name} className="custom-field-item">
                    <span>{field.label}</span>
                    <button 
                      className="btn-remove"
                      onClick={() => removeCustomField(field.name)}
                    >
                      ×
                    </button>
                  </div>
                ))}
                <button className="btn-add-field" onClick={addCustomField}>
                  + Agregar campo personalizado
                </button>
              </div>
            </div>

            <div className="config-section">
              <label className="field-checkbox">
                <input
                  type="checkbox"
                  checked={authConfig.require_verification}
                  onChange={(e) => setAuthConfig(prev => ({ 
                    ...prev, 
                    require_verification: e.target.checked 
                  }))}
                />
                <span>Requerir verificación de email</span>
              </label>
            </div>

            <button className="btn-save" onClick={saveAuthConfig}>
              Guardar Configuración
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

function getModuleIcon(icon: string): string {
  const icons: Record<string, string> = {
    "shield": "🔐",
    "box": "📦",
    "shopping-cart": "🛒",
    "file-text": "📄",
    "bar-chart": "📊",
    "users": "👥",
    "settings": "⚙️",
    "edit": "📝", // 👈 Añadido para el blog
  };
  return icons[icon] || "📦";
}

export default Modulos;