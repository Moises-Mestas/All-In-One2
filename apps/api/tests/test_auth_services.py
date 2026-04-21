import pytest
import time
from decimal import Decimal
from packages.modules.auth.services import AuthService
from packages.modules.auth.schemas import (
    SiteUserRegister, SiteUserLogin, ForgotPasswordRequest, ResetPasswordRequest, RefreshTokenRequest
)


def generate_email():
    return f"test_{int(time.time() * 1000)}@mail.com"


@pytest.mark.asyncio
async def test_register_success(db_session):
    service = AuthService(db_session, site_id=1)
    
    user = await service.register(SiteUserRegister(
        email=generate_email(),
        password="123456",
        first_name="Test",
        last_name="User"
    ))
    
    assert user.id is not None
    assert user.email is not None
    assert user.first_name == "Test"


@pytest.mark.asyncio
async def test_register_duplicate_email(db_session):
    service = AuthService(db_session, site_id=1)
    email = generate_email()
    
    await service.register(SiteUserRegister(
        email=email,
        password="123456",
        first_name="Test"
    ))
    
    with pytest.raises(ValueError, match="ya está registrado"):
        await service.register(SiteUserRegister(
            email=email,
            password="123456",
            first_name="Test"
        ))


@pytest.mark.asyncio
async def test_login_success(db_session):
    service = AuthService(db_session, site_id=1)
    email = generate_email()
    
    await service.register(SiteUserRegister(
        email=email,
        password="mipassword",
        first_name="Test"
    ))
    
    user, tokens = await service.login(email, "mipassword", user_agent="test", ip="127.0.0.1")
    
    assert user.email == email
    assert "access_token" in tokens
    assert tokens["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_email(db_session):
    service = AuthService(db_session, site_id=1)
    
    with pytest.raises(ValueError, match="incorrectos"):
        await service.login("noexiste@mail.com", "password")


@pytest.mark.asyncio
async def test_login_invalid_password(db_session):
    service = AuthService(db_session, site_id=1)
    email = generate_email()
    
    await service.register(SiteUserRegister(
        email=email,
        password="password123",
        first_name="Test"
    ))
    
    with pytest.raises(ValueError, match="incorrectos"):
        await service.login(email, "passwordincorrecto")


@pytest.mark.asyncio
async def test_logout(db_session):
    service = AuthService(db_session, site_id=1)
    email = generate_email()
    
    await service.register(SiteUserRegister(email=email, password="123456"))
    user, tokens = await service.login(email, "123456", user_agent="test")
    
    result = await service.logout(tokens["access_token"])
    assert result is True
    
    result2 = await service.logout("token_invalido")
    assert result2 is False


@pytest.mark.asyncio
async def test_get_current_user(db_session):
    service = AuthService(db_session, site_id=1)
    email = generate_email()
    
    await service.register(SiteUserRegister(email=email, password="123456"))
    user, tokens = await service.login(email, "123456")
    
    current = await service.get_current_user(tokens["access_token"])
    assert current is not None
    assert current.email == email
    
    invalid = await service.get_current_user("token_invalido")
    assert invalid is None


@pytest.mark.asyncio
async def test_refresh_tokens(db_session):
    service = AuthService(db_session, site_id=1)
    email = generate_email()
    
    await service.register(SiteUserRegister(email=email, password="123456"))
    user, tokens = await service.login(email, "123456")
    
    new_tokens = await service.refresh_tokens(tokens["refresh_token"])
    
    assert "access_token" in new_tokens
    assert new_tokens["access_token"] != tokens["access_token"]


@pytest.mark.asyncio
async def test_refresh_tokens_invalid(db_session):
    service = AuthService(db_session, site_id=1)
    
    with pytest.raises(ValueError, match="inválido"):
        await service.refresh_tokens("token_invalido")


@pytest.mark.asyncio
async def test_forgot_password(db_session):
    service = AuthService(db_session, site_id=1)
    email = generate_email()
    
    user = await service.register(SiteUserRegister(email=email, password="123456"))
    
    token = await service.forgot_password(email)
    assert token is not None
    
    no_user = await service.forgot_password("noexiste@mail.com")
    assert no_user is None


@pytest.mark.asyncio
async def test_reset_password(db_session):
    service = AuthService(db_session, site_id=1)
    email = generate_email()
    
    await service.register(SiteUserRegister(email=email, password="password123"))
    
    token = await service.forgot_password(email)
    result = await service.reset_password(token, "nuevapass")
    assert result is True
    
    user, tokens = await service.login(email, "nuevapass")
    assert user is not None


@pytest.mark.asyncio
async def test_reset_password_invalid_token(db_session):
    service = AuthService(db_session, site_id=1)
    
    result = await service.reset_password("token_invalido", "nuevapass")
    assert result is False
