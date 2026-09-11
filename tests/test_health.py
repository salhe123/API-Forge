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
    assert response.json() == {"status": "the backend is healthy", "database": "ok"}
    assert response.headers.get("X-Request-ID")
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert float(response.headers["X-Response-Time-Ms"]) >= 0


def test_unknown_route_returns_json_404(client):
    response = client.get("/no-such-route")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}
