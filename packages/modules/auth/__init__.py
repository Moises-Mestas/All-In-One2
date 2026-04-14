from packages.core.plugin_base import Module
from packages.modules.auth.models import SiteUser, AuthSession, PasswordResetToken
from packages.modules.auth.schemas import (
    SiteUserRegister,
    SiteUserLogin,
    SiteUserResponse,
    TokenResponse,
    AuthConfigResponse,
)


class AuthModule(Module):
    name = "Auth"
    slug = "auth"
    version = "1.0.0"
    description = "Sistema de autenticación para sitios públicos"
    icon = "shield"
    admin_url = "/admin/auth"
    is_system = False

    def get_models(self):
        return [SiteUser, AuthSession, PasswordResetToken]

    def get_schemas(self):
        return {
            "SiteUser": SiteUser,
            "SiteUserRegister": SiteUserRegister,
            "SiteUserLogin": SiteUserLogin,
            "SiteUserResponse": SiteUserResponse,
            "TokenResponse": TokenResponse,
            "AuthConfigResponse": AuthConfigResponse,
        }

    def get_admin_menu(self):
        return [
            {
                "title": "Configuración de Auth",
                "url": f"{self.admin_url}/settings",
                "icon": self.icon,
            }
        ]


module = AuthModule()
