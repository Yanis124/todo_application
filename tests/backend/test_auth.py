import pytest
from fastapi import status


class TestRegister:
    def test_register_success(self, client):
        response = client.post("/api/auth/register", json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123"
        })
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == "newuser"
        assert data["email"] == "new@example.com"
        assert "id" in data
        assert "hashed_password" not in data

    def test_register_duplicate_username(self, client, test_user):
        response = client.post("/api/auth/register", json={
            "username": "testuser",
            "email": "other@example.com",
            "password": "password123"
        })
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "Username already registered" in response.json()["detail"]

    def test_register_duplicate_email(self, client, test_user):
        response = client.post("/api/auth/register", json={
            "username": "otheruser",
            "email": "test@example.com",
            "password": "password123"
        })
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "Email already registered" in response.json()["detail"]

    def test_register_short_username(self, client):
        response = client.post("/api/auth/register", json={
            "username": "ab",
            "email": "short@example.com",
            "password": "password123"
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_register_short_password(self, client):
        response = client.post("/api/auth/register", json={
            "username": "validuser",
            "email": "valid@example.com",
            "password": "12345"
        })
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestLogin:
    def test_login_success(self, client, test_user):
        response = client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "testpassword123"
        })
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, test_user):
        response = client.post("/api/auth/login", json={
            "email": "test@example.com",
            "password": "wrongpassword"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user(self, client):
        response = client.post("/api/auth/login", json={
            "email": "nonexistent@example.com",
            "password": "password123"
        })
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestGetMe:
    def test_get_me_authenticated(self, client, test_user, auth_headers):
        response = client.get("/api/auth/me", headers=auth_headers)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"

    def test_get_me_unauthenticated(self, client):
        response = client.get("/api/auth/me")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_me_invalid_token(self, client):
        response = client.get("/api/auth/me", headers={"Authorization": "Bearer invalidtoken"})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
