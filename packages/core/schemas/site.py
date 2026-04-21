from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

class SiteBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    slug: str = Field(..., min_length=1, max_length=255, pattern=r"^[a-z0-9-]+$")
    settings: Optional[Dict[str, Any]] = None
    
    # 👇 LE DAMOS PERMISO DE LEER ESTOS DATOS
    is_template: bool = False 

class SiteCreate(SiteBase):
    template_id: Optional[int] = None # 👇 Permiso para recibir qué plantilla clonar

class SiteUpdate(BaseModel):
    settings: Optional[Dict[str, Any]] = None
    name: Optional[str] = None
    is_template: Optional[bool] = None

class SiteResponse(SiteBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)