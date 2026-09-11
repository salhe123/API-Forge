def test_register_and_login(client):
    created = client.post(
        "/api/v1/auth/register",
        json={"email": "forge@example.com", "password": "secret123"},
    )
    assert created.status_code == 201
    body = created.json()
    assert created.headers["Location"] == "/api/v1/auth/me"
    assert body["email"] == "forge@example.com"
    assert "password" not in body
    assert "hashed_password" not in body

    login = client.post(
        "/api/v1/auth/login",
        json={"email": "forge@example.com", "password": "secret123"},
    )
    assert login.status_code == 200
    token = login.json()
    assert token["token_type"] == "bearer"
    assert token["access_token"]
    assert token["expires_in"] == 3600
    assert login.headers["Cache-Control"] == "no-store"


def test_register_duplicate_email(client):
    payload = {"email": "forge@example.com", "password": "secret123"}
    client.post("/api/v1/auth/register", json=payload)
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 409
    assert response.json()["detail"] == "Email already registered"


def test_login_rejects_bad_password(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "forge@example.com", "password": "secret123"},
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "forge@example.com", "password": "wrongpass"},
    )
    assert response.status_code == 401


def test_me_requires_token(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401
    assert response.headers["Cache-Control"] == "no-store"


def test_me_returns_current_user(client, auth_headers):
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["email"] == "forge@example.com"


def test_login_accepts_email_with_different_case(client):
    created = client.post(
        "/api/v1/auth/register",
        json={"email": "Forge@Example.com", "password": "secret123"},
    )
    assert created.status_code == 201
    assert created.json()["email"] == "forge@example.com"
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "forge@example.com", "password": "secret123"},
    )
    assert response.status_code == 200
    assert response.json()["access_token"]
