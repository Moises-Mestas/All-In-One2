import api from './api';

const BASE_PATH = '/api/v1/templates';

export const templatesService = {
  getAll: async () => {
    const { data } = await api.get(`${BASE_PATH}`);
    return data;
  },
  getById: async (id: number) => {
    const { data } = await api.get(`${BASE_PATH}/${id}`);
    return data;
  },
  create: async (templateData: any) => {
    const { data } = await api.post(`${BASE_PATH}`, templateData);
    return data;
  },
  // 👇 ESTA ES LA FUNCIÓN QUE FALTABA PARA PODER GUARDAR 👇
  update: async (id: number, templateData: any) => {
    const { data } = await api.put(`${BASE_PATH}/${id}`, templateData);
    return data;
  },
  delete: async (id: number) => {
    const { data } = await api.delete(`${BASE_PATH}/${id}`);
    return data;
  }
};