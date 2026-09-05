def test_create_and_get_item(client):
    created = client.post(
        "/api/v1/items/",
        json={"name": "Steel Blade", "description": "First forging", "strength": 40},
    )
    assert created.status_code == 201
    body = created.json()
    assert body["id"] == 1
    assert body["name"] == "Steel Blade"

    fetched = client.get("/api/v1/items/1")
    assert fetched.status_code == 200
    assert fetched.json() == body


def test_list_items_filters_by_min_strength(client):
    client.post("/api/v1/items/", json={"name": "Soft Iron", "strength": 10})
    client.post("/api/v1/items/", json={"name": "Hard Steel", "strength": 80})

    response = client.get("/api/v1/items/", params={"min_strength": 50})
    assert response.status_code == 200
    names = [item["name"] for item in response.json()]
    assert names == ["Hard Steel"]


def test_update_item(client):
    client.post("/api/v1/items/", json={"name": "Draft", "strength": 5})
    response = client.put(
        "/api/v1/items/1",
        json={"name": "Finished", "description": "Tempered", "strength": 70},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Finished"
    assert response.json()["strength"] == 70


def test_delete_item(client):
    client.post("/api/v1/items/", json={"name": "Scrap"})
    deleted = client.delete("/api/v1/items/1")
    assert deleted.status_code == 204

    missing = client.get("/api/v1/items/1")
    assert missing.status_code == 404
    assert missing.json()["detail"] == "Item not found"


def test_missing_item_returns_404(client):
    response = client.get("/api/v1/items/99")
    assert response.status_code == 404


def test_create_rejects_invalid_strength(client):
    response = client.post("/api/v1/items/", json={"name": "Broken", "strength": 0})
    assert response.status_code == 422
