from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime

class TemplateBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    settings: Optional[Any] = None
    thumbnail_url: Optional[str] = None
    is_active: bool = True

class TemplateCreate(TemplateBase):
    pass

class TemplateUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    settings: Optional[Any] = None
    thumbnail_url: Optional[str] = None
    is_active: Optional[bool] = None

class TemplateResponse(TemplateBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)