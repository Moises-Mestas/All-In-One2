from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response, HTMLResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from packages.core.models.site import Site


def extract_subdomain(host: str) -> str | None:
    if not host:
        return None
    
    parts = host.split(".")
    
    if len(parts) >= 3:
        if parts[-2] == "localtest" and parts[-1] == "me":
            return parts[0]
        if "nip.io" in host:
            return parts[0]
        if parts[0] not in ["www", "api", "admin"]:
            return parts[0]
    
    return None


class SubdomainMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        host = request.headers.get("host", "")
        subdomain = extract_subdomain(host)
        
        if subdomain:
            request.state.subdomain = subdomain
            request.state.is_site_request = True
        else:
            request.state.subdomain = None
            request.state.is_site_request = False
        
        response = await call_next(request)
        return response
