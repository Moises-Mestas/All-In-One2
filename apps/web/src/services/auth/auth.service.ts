import api from "../api";
import type { User, UserRegister, UserLogin, TokenResponse } from "../../types";

export const authService = {
  register: async (data: UserRegister): Promise<User> => {
    const response = await api.post<User>("/auth/register", data);
    return response.data;
  },

  login: async (data: UserLogin): Promise<TokenResponse> => {
    const response = await api.post<TokenResponse>("/auth/login", data);
    const { access_token } = response.data;
    localStorage.setItem("token", access_token);
    return response.data;
  },

  getMe: async (): Promise<User> => {
    const response = await api.get<User>("/auth/me");
    localStorage.setItem("user", JSON.stringify(response.data));
    return response.data;
  },

  logout: () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
  },
};
