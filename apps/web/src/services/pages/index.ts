import api from "../api";
import type { Page, PageCreate, PageUpdate } from "../../types";

export const pagesService = {
  async getAll(siteId: number): Promise<Page[]> {
    const { data } = await api.get(`/pages/site/${siteId}`);
    return data;
  },

  async get(id: number): Promise<Page> {
    const { data } = await api.get(`/pages/${id}`);
    return data;
  },

  async create(page: PageCreate): Promise<Page> {
    const { data } = await api.post("/pages", page);
    return data;
  },

  async update(id: number, page: PageUpdate): Promise<Page> {
    const { data } = await api.put(`/pages/${id}`, page);
    return data;
  },

  async delete(id: number): Promise<void> {
    await api.delete(`/pages/${id}`);
  },

  async saveEditor(id: number, gjsData: string, gjsHtml: string, gjsCss: string): Promise<Page> {
    const { data } = await api.post(`/pages/${id}/save-editor`, null, {
      params: { gjs_data: gjsData, gjs_html: gjsHtml, gjs_css: gjsCss },
    });
    return data;
  },
};
