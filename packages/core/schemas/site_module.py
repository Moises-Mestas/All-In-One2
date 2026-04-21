from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict



class SiteModuleBase(BaseModel):
    site_id: int
    module_id: int
    is_active: Optional[bool] = False
    config: Optional[Dict[str, Any]] = None


class SiteModuleCreate(SiteModuleBase):
    pass


class SiteModuleUpdate(BaseModel):
    site_id: Optional[int] = None
    module_id: Optional[int] = None
    is_active: Optional[bool] = None
    config: Optional[Dict[str, Any]] = None
    activated_at: Optional[datetime] = None
    deactivated_at: Optional[datetime] = None

class SiteModuleResponse(SiteModuleBase):
    id: int
    activated_at: Optional[datetime] = None
    deactivated_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)    