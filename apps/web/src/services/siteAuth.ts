import axios from "axios";

const getApiUrl = (siteId: number) => `http://localhost:8000/api/v1/sites/${siteId}/auth`;

export interface AuthConfig {
  registration_fields: string[];
  custom_fields: Array<{ name: string; label: string }>;
  require_verification: boolean;
}

export interface SiteUser {
  id: number;
  email: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
  custom_fields: Record<string, any>;
  created_at: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface RegisterData {
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
  phone?: string;
  custom_fields?: Record<string, any>;
}

export interface LoginData {
  email: string;
  password: string;
}

class SiteAuthService {
  private siteId: number;

  constructor(siteId: number) {
    this.siteId = siteId;
  }

  private getApi() {
    const api = axios.create({
      baseURL: getApiUrl(this.siteId),
      headers: {
        "Content-Type": "application/json",
      },
    });

    api.interceptors.request.use((config) => {
      const token = this.getToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          this.logout();
        }
        return Promise.reject(error);
      }
    );

    return api;
  }

  getToken(): string | null {
    return localStorage.getItem(`site_${this.siteId}_token`);
  }

  getRefreshToken(): string | null {
    return localStorage.getItem(`site_${this.siteId}_refresh_token`);
  }

  setTokens(tokens: TokenResponse) {
    localStorage.setItem(`site_${this.siteId}_token`, tokens.access_token);
    localStorage.setItem(`site_${this.siteId}_refresh_token`, tokens.refresh_token);
    localStorage.setItem(`site_${this.siteId}_token_expires`, 
      String(Date.now() + tokens.expires_in * 1000)
    );
  }

  clearTokens() {
    localStorage.removeItem(`site_${this.siteId}_token`);
    localStorage.removeItem(`site_${this.siteId}_refresh_token`);
    localStorage.removeItem(`site_${this.siteId}_token_expires`);
    localStorage.removeItem(`site_${this.siteId}_user`);
  }

  isAuthenticated(): boolean {
    const token = this.getToken();
    const expires = localStorage.getItem(`site_${this.siteId}_token_expires`);
    
    if (!token) return false;
    if (expires && Date.now() > parseInt(expires)) {
      this.clearTokens();
      return false;
    }
    return true;
  }

  getUser(): SiteUser | null {
    const userStr = localStorage.getItem(`site_${this.siteId}_user`);
    return userStr ? JSON.parse(userStr) : null;
  }

  setUser(user: SiteUser) {
    localStorage.setItem(`site_${this.siteId}_user`, JSON.stringify(user));
  }

  async getConfig(): Promise<AuthConfig> {
    const api = this.getApi();
    const { data } = await api.get("/config");
    return data;
  }

  async register(userData: RegisterData): Promise<SiteUser> {
    const api = this.getApi();
    const { data } = await api.post("/register", userData);
    return data;
  }

  async login(credentials: LoginData): Promise<TokenResponse> {
    const api = this.getApi();
    const { data } = await api.post("/login", credentials);
    
    this.setTokens(data);
    
    try {
      const user = await this.getCurrentUser();
      this.setUser(user);
    } catch (error) {
      console.error("Error fetching user after login:", error);
    }
    
    return data;
  }

  async logout(): Promise<void> {
    try {
      const api = this.getApi();
      await api.post("/logout");
    } catch (error) {
      console.error("Error during logout:", error);
    } finally {
      this.clearTokens();
    }
  }

  async getCurrentUser(): Promise<SiteUser> {
    const api = this.getApi();
    const { data } = await api.get("/me");
    this.setUser(data);
    return data;
  }

  async refreshTokens(): Promise<TokenResponse> {
    const refreshToken = this.getRefreshToken();
    if (!refreshToken) {
      throw new Error("No refresh token available");
    }

    const api = this.getApi();
    const { data } = await api.post("/refresh", { refresh_token: refreshToken });
    this.setTokens(data);
    return data;
  }

  async forgotPassword(email: string): Promise<void> {
    const api = this.getApi();
    await api.post("/forgot-password", { email });
  }

  async resetPassword(token: string, newPassword: string): Promise<void> {
    const api = this.getApi();
    await api.post("/reset-password", { token, new_password: newPassword });
  }
}

export default SiteAuthService;
