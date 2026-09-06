def test_hello(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello API Forge"}


def test_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "the backend is healthy"}
    assert response.headers.get("X-Request-ID")


def test_unknown_route_returns_json_404(client):
    response = client.get("/no-such-route")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not found"}
