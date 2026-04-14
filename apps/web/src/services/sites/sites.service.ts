import api from "../api"; 
import type { Site } from "../../types";

// 👇 VOLVEMOS A LA RUTA ORIGINAL DE TU BACKEND PARA QUE VUELVA A FUNCIONAR
const BASE_PATH = '/sites';

export const sitesService = {
  getAll: async (): Promise<Site[]> => {
    const response = await api.get(BASE_PATH);
    return response.data;
  },
  
  getById: async (id: number): Promise<Site> => {
    const response = await api.get(`${BASE_PATH}/${id}`);
    return response.data;
  },

  getActiveModules: async (siteId: number): Promise<string[]> => {
    const response = await api.get(`/site-modules/site/${siteId}`);
    const modules = response.data
      .filter((sm: any) => sm.is_active)
      .map((sm: any) => sm.module?.slug)
      .filter(Boolean);
    return modules;
  },

  create: async (data: { 
    name: string; 
    slug: string; 
    is_template?: boolean; 
    template_id?: number | string | null;
    settings?: any; 
  }): Promise<Site> => {
    
    // 🛡️ Filtramos los datos estrictamente para que FastAPI no lance error 422
    const payload: any = {
      name: data.name,
      slug: data.slug,
      is_template: data.is_template || false,
    };

    if (data.template_id) payload.template_id = Number(data.template_id);
    if (data.settings) payload.settings = data.settings; // Solo se envía si existe

    const response = await api.post(BASE_PATH, payload);
    return response.data;
  },

  update: async (id: number, data: { settings?: any; name?: string; is_template?: boolean }): Promise<Site> => {
    const response = await api.put(`${BASE_PATH}/${id}`, data);
    return response.data;
  },

  delete: async (id: number): Promise<void> => {
    await api.delete(`${BASE_PATH}/${id}`);
  }
};