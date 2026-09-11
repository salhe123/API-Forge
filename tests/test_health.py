def test_hello(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello API Forge"}


def test_api_v1_root(client):
    response = client.get("/api/v1/")
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "API Forge"
    assert body["version"] == "0.1.0"
    assert body["docs"] == "/docs"


def test_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "the backend is healthy",
        "database": "ok",
        "version": "0.1.0",
    }
    assert response.headers.get("X-Request-ID")
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("X-API-Version") == "0.1.0"
    assert float(response.headers["X-Response-Time-Ms"]) >= 0


def test_cors_exposes_custom_headers(client):
    response = client.get("/api/v1/health", headers={"Origin": "http://localhost:4200"})
    assert response.status_code == 200
    exposed = response.headers.get("access-control-expose-headers", "")
    assert "Location" in exposed
    assert "X-API-Version" in exposed
    assert "X-Request-ID" in exposed
    assert "X-Response-Time-Ms" in exposed
    assert "X-Total-Count" in exposed


def test_unknown_route_returns_json_404(client):
    response = client.get("/no-such-route")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}
