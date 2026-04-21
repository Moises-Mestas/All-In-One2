import api from "./api";

export interface Module {
  id: number;
  name: string;
  slug: string;
  description: string;
  version: string;
  is_system: boolean;
  is_active: boolean;
  icon: string;
  config_schema: Record<string, any>;
  admin_url: string;
  created_at: string;
  updated_at: string;
}

export interface SiteModule {
  id: number;
  site_id: number;
  module_id: number;
  is_active: boolean;
  config: Record<string, any>;
  activated_at: string;
  deactivated_at: string;
  created_at: string;
  updated_at: string;
}

export interface AuthConfig {
  registration_fields: string[];
  custom_fields: Array<{ name: string; label: string }>;
  require_verification: boolean;
}

export const modulesService = {
  getAll: async (): Promise<Module[]> => {
    const { data } = await api.get("/modules");
    return data;
  },

  getById: async (id: number): Promise<Module> => {
    const { data } = await api.get(`/modules/${id}`);
    return data;
  },

  create: async (module: Partial<Module>): Promise<Module> => {
    const { data } = await api.post("/modules", module);
    return data;
  },

  update: async (id: number, module: Partial<Module>): Promise<Module> => {
    const { data } = await api.put(`/modules/${id}`, module);
    return data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/modules/${id}`);
  },
};

export const siteModulesService = {
  getBySite: async (siteId: number): Promise<SiteModule[]> => {
    const { data } = await api.get(`/site-modules/site/${siteId}`);
    return data;
  },

  create: async (siteModule: Partial<SiteModule>): Promise<SiteModule> => {
    const { data } = await api.post("/site-modules", siteModule);
    return data;
  },

  update: async (id: number, siteModule: Partial<SiteModule>): Promise<SiteModule> => {
    const { data } = await api.put(`/site-modules/${id}`, siteModule);
    return data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`/site-modules/${id}`);
  },

  toggle: async (id: number): Promise<SiteModule> => {
    const { data } = await api.post(`/site-modules/${id}/toggle`);
    return data;
  },

  activateModule: async (siteId: number, moduleSlug: string): Promise<SiteModule> => {
    const { data } = await api.post(`/site-modules/site/${siteId}/activate-module/${moduleSlug}`);
    return data;
  },

  getAuthConfig: async (siteId: number): Promise<AuthConfig> => {
    const { data } = await api.get(`/api/v1/sites/${siteId}/auth/config`);
    return data;
  },
};

export const authModuleService = {
  AVAILABLE_FIELDS: [
    { value: "email", label: "Email", required: true },
    { value: "password", label: "Contraseña", required: true },
    { value: "first_name", label: "Nombre", required: false },
    { value: "last_name", label: "Apellido", required: false },
    { value: "phone", label: "Teléfono", required: false },
    { value: "address", label: "Dirección", required: false },
    { value: "company", label: "Empresa", required: false },
  ],

  getDefaultConfig: (): AuthConfig => ({
    registration_fields: ["email", "password", "first_name", "last_name"],
    custom_fields: [],
    require_verification: false,
  }),

  updateAuthConfig: async (siteId: number, config: AuthConfig): Promise<void> => {
    const siteModules = await siteModulesService.getBySite(siteId);
    const authModule = siteModules.find((sm: SiteModule) => {
      return true;
    });
    
    if (authModule) {
      await siteModulesService.update(authModule.id, { config });
    }
  },
};
