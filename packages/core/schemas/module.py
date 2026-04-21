from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict


class ModuleBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None
    version: str = "1.0.0"
    is_system: bool = False
    is_active: bool = True
    icon: str = "box"
    config_schema: Dict[str, Any] = {}
    admin_url: Optional[str] = None

class ModuleCreate(ModuleBase):
    pass

class ModuleUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    version: Optional[str] = None
    is_system: Optional[bool] = None
    is_active: Optional[bool] = None
    icon: Optional[str] = None
    config_schema: Optional[Dict[str, Any]] = None
    admin_url: Optional[str] = None

class ModuleResponse(ModuleBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)