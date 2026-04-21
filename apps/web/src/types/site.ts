export interface Site {
  settings(settings: any): unknown;
  id: number;
  name: string;
  slug: string;
  user_id: number;
  created_at: string;
  updated_at: string;
}

export interface SiteCreate {
  name: string;
  slug: string;
}
