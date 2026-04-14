import pytest
from packages.shared.site_scripts.auth.register_btn import get_auth_script, get_register_script
from packages.shared.site_scripts.store import get_store_card_script as get_store_script


def test_get_auth_script_basic():
    script = get_auth_script(site_id=1)
    assert script is not None
    assert len(script) > 0
    assert "siteId = 1" in script


def test_get_auth_script_custom_fields():
    script = get_auth_script(site_id=1, registration_fields=["email", "password"])
    assert script is not None
    assert "email" in script


def test_get_register_script():
    script = get_register_script(site_id=1, site_slug="test")
    assert script is not None
    assert len(script) > 0


def test_get_store_script():
    script = get_store_script(site_id=1)
    assert script is not None
    assert len(script) > 0