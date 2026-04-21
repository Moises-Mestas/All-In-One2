import pytest
import time
from pydantic import EmailStr


def generate_email():
    return f"test_{int(time.time() * 1000)}@example.com"


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    email = generate_email()
    await client.post("/auth/register", json={
        "email": email,
        "password": "123456"
    })
    resp = await client.post("/auth/login", json={
        "email": email,
        "password": "wrongpassword"
    })
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_login_wrong_email(client):
    resp = await client.post("/auth/login", json={
        "email": "noexiste@example.com",
        "password": "123456"
    })
    assert resp.status_code == 401