export interface Page {
  id: number;
  site_id: number;
  title: string;
  slug: string;
  content: string;
  gjs_data: string | null;
  gjs_html: string | null;
  gjs_css: string | null;
  is_home: boolean;
  is_published: boolean;
  meta_title: string | null;
  meta_description: string | null;
  created_at: string;
  updated_at: string;
}

export interface PageCreate {
  site_id: number;
  title: string;
  slug: string;
  content?: string;
  is_home?: boolean;
  is_published?: boolean;
  meta_title?: string;
  meta_description?: string;
}

export interface PageUpdate {
  title?: string;
  slug?: string;
  content?: string;
  gjs_data?: string;
  gjs_html?: string;
  gjs_css?: string;
  is_home?: boolean;
  is_published?: boolean;
  meta_title?: string;
  meta_description?: string;
}
