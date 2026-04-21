from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from packages.modules.blog.models import PostStatus

# --- SCHEMAS PARA CATEGORÍAS ---
class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass # El slug lo generaremos automáticamente en el servicio

class CategoryResponse(CategoryBase):
    id: int
    site_id: int
    slug: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# --- SCHEMAS PARA POSTS (ARTÍCULOS) ---
class PostBase(BaseModel):
    title: str = Field(..., max_length=255)
    content: str
    excerpt: Optional[str] = None
    featured_image: Optional[str] = None
    status: PostStatus = PostStatus.DRAFT
    published_at: Optional[datetime] = None
    category_id: Optional[int] = None
    
    # SEO
    meta_title: Optional[str] = Field(None, max_length=255)
    meta_description: Optional[str] = None

class PostCreate(PostBase):
    pass # El slug se genera solo

class PostUpdate(PostBase):
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None

class PostResponse(PostBase):
    id: int
    site_id: int
    slug: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)