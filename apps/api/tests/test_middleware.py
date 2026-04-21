import pytest
from starlette.middleware.base import BaseHTTPMiddleware
from app.middleware.subdomain import extract_subdomain, SubdomainMiddleware


def test_extract_subdomain_basic():
    assert extract_subdomain("test.example.com") == "test"


def test_extract_subdomain_www():
    assert extract_subdomain("www.example.com") is None


def test_extract_subdomain_api():
    assert extract_subdomain("api.example.com") is None


def test_extract_subdomain_admin():
    assert extract_subdomain("admin.example.com") is None


def test_extract_subdomain_nipio():
    assert extract_subdomain("192.168.1.1.nip.io") == "192"


def test_extract_subdomain_empty():
    assert extract_subdomain("") is None


def test_extract_subdomain_none():
    assert extract_subdomain(None) is None


def test_extract_subdomain_localtest_me():
    assert extract_subdomain("mysite.localtest.me") == "mysite"


def test_subdomain_middleware_class():
    assert issubclass(SubdomainMiddleware, BaseHTTPMiddleware)