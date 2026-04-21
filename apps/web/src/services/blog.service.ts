// apps/web/src/services/blog.service.ts
import api from './api'; // Tu instancia de Axios preconfigurada

// 💡 El truco: Forzamos la ruta exacta para evitar que el proxy del frontend se confunda
const BASE_PATH = '/modules/blog';

export const blogService = {
  // 1. Obtener todos los artículos
  getPosts: async (siteId: number) => {
    const { data } = await api.get(`${BASE_PATH}/${siteId}/posts`);
    return data;
  },

  // 2. Crear un nuevo artículo
  createPost: async (siteId: number, postData: any) => {
    const { data } = await api.post(`${BASE_PATH}/${siteId}/posts`, postData);
    return data;
  },

  // 3. Actualizar artículo
  updatePost: async (siteId: number, postId: number, postData: any) => {
    const { data } = await api.put(`${BASE_PATH}/${siteId}/posts/${postId}`, postData);
    return data;
  },

  // 4. Borrar artículo
  deletePost: async (siteId: number, postId: number) => {
    const { data } = await api.delete(`${BASE_PATH}/${siteId}/posts/${postId}`);
    return data;
  },

  // 5. Subir imagen (La que ya funcionaba)
  uploadImage: async (siteId: number, file: File) => {
    const formData = new FormData();
    formData.append("file", file);
    
    const { data } = await api.post(`${BASE_PATH}/${siteId}/upload-image`, formData, {
      headers: { "Content-Type": "multipart/form-data" }
    });
    return data.url; 
  }
};