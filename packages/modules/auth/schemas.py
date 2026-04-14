from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class AuthConfigBase(BaseModel):
    registration_fields: List[str] = ["email", "password"]
    custom_fields: List[Dict[str, str]] = []
    require_verification: bool = False


class AuthConfigUpdate(BaseModel):
    registration_fields: Optional[List[str]] = None
    custom_fields: Optional[List[Dict[str, str]]] = None
    require_verification: Optional[bool] = None


class AuthConfigResponse(BaseModel):
    registration_fields: List[str]
    custom_fields: List[Dict[str, str]]
    require_verification: bool


class SiteUserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    custom_fields: Optional[Dict[str, Any]] = {}


class SiteUserLogin(BaseModel):
    email: EmailStr
    password: str


class SiteUserResponse(BaseModel):
    id: int
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    custom_fields: Dict[str, Any] = {}
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int
    user: Optional[SiteUserResponse] = None


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(..., min_length=6)


class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str = Field(..., min_length=6)


class AuthStatusResponse(BaseModel):
    is_authenticated: bool
    user: Optional[SiteUserResponse] = None
    config: Optional[AuthConfigResponse] = None
