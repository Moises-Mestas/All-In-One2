from typing import List, Dict, Any
import json

from .auth.register_btn import get_auth_script
from .store import get_store_card_script


def get_site_scripts(
    site_id: int,
    site_slug: str,
    html_content: str,
    auth_config: Dict[str, Any] = None
) -> str:
    scripts = []
    
    if auth_config:
        if isinstance(auth_config, str):
            try:
                auth_config = json.loads(auth_config)
            # 👇 CORRECCIÓN: Especificamos el tipo de error
            except json.JSONDecodeError:
                auth_config = None
    
    has_login = "auth-login-btn" in html_content
    has_register = "auth-register-btn" in html_content
    has_user_info = "auth-user-info" in html_content
    
    if has_login or has_register or has_user_info:
        registration_fields = ["email", "password", "first_name", "last_name"]
        custom_fields = []
        
        if auth_config:
            registration_fields = auth_config.get("registration_fields") or ["email", "password", "first_name", "last_name"]
            custom_fields = auth_config.get("custom_fields") or []
        
        scripts.append(get_auth_script(
            site_id=site_id,
            registration_fields=registration_fields,
            custom_fields=custom_fields
        ))
    
    # Script para tienda (productos, carrito, checkout)
    has_tienda = "tienda-agregar-btn" in html_content or "tienda-mini-carrito" in html_content or 'data-gjs-type="tienda-carrito"' in html_content
    if has_tienda:
        scripts.append(get_store_card_script(site_id))
    
    return "\n".join(scripts)


__all__ = ["get_site_scripts"]