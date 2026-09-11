def test_create_and_get_item(client, auth_headers):
    created = client.post(
        "/api/v1/items/",
        headers=auth_headers,
        json={"name": "Steel Blade", "description": "First forging", "strength": 40},
    )
    assert created.status_code == 201
    body = created.json()
    assert created.headers["Location"] == "/api/v1/items/1"
    assert body["id"] == 1
    assert body["name"] == "Steel Blade"
    assert body["owner_id"] == 1

    fetched = client.get("/api/v1/items/1")
    assert fetched.status_code == 200
    assert fetched.json() == body


def test_list_items_filters_by_min_strength(client, auth_headers):
    client.post(
        "/api/v1/items/",
        headers=auth_headers,
        json={"name": "Soft Iron", "strength": 10},
    )
    client.post(
        "/api/v1/items/",
        headers=auth_headers,
        json={"name": "Hard Steel", "strength": 80},
    )

    response = client.get("/api/v1/items/", params={"min_strength": 50})
    assert response.status_code == 200
    names = [item["name"] for item in response.json()]
    assert names == ["Hard Steel"]


def test_list_items_filters_by_max_strength(client, auth_headers):
    client.post("/api/v1/items/", headers=auth_headers, json={"name": "Soft Iron", "strength": 10})
    client.post("/api/v1/items/", headers=auth_headers, json={"name": "Hard Steel", "strength": 80})

    response = client.get("/api/v1/items/", params={"max_strength": 20})
    assert response.status_code == 200
    names = [item["name"] for item in response.json()]
    assert names == ["Soft Iron"]


def test_list_items_supports_skip_and_limit(client, auth_headers):
    client.post("/api/v1/items/", headers=auth_headers, json={"name": "One"})
    client.post("/api/v1/items/", headers=auth_headers, json={"name": "Two"})
    client.post("/api/v1/items/", headers=auth_headers, json={"name": "Three"})

    response = client.get("/api/v1/items/", params={"skip": 1, "limit": 1})
    assert response.status_code == 200
    names = [item["name"] for item in response.json()]
    assert names == ["Two"]
    assert response.headers["X-Total-Count"] == "3"


def test_list_items_searches_by_name(client, auth_headers):
    client.post("/api/v1/items/", headers=auth_headers, json={"name": "Steel Blade"})
    client.post("/api/v1/items/", headers=auth_headers, json={"name": "Copper Pan"})

    response = client.get("/api/v1/items/", params={"q": "steel"})
    assert response.status_code == 200
    names = [item["name"] for item in response.json()]
    assert names == ["Steel Blade"]


def test_list_items_sorts_by_strength_desc(client, auth_headers):
    client.post("/api/v1/items/", headers=auth_headers, json={"name": "Soft", "strength": 10})
    client.post("/api/v1/items/", headers=auth_headers, json={"name": "Hard", "strength": 90})

    response = client.get("/api/v1/items/", params={"sort": "-strength"})
    assert response.status_code == 200
    names = [item["name"] for item in response.json()]
    assert names == ["Hard", "Soft"]


def test_list_items_filters_by_owner_id(client, auth_headers, other_auth_headers):
    client.post("/api/v1/items/", headers=auth_headers, json={"name": "Mine"})
    client.post("/api/v1/items/", headers=other_auth_headers, json={"name": "Theirs"})

    response = client.get("/api/v1/items/", params={"owner_id": 1})
    assert response.status_code == 200
    names = [item["name"] for item in response.json()]
    assert names == ["Mine"]


def test_create_item_strips_name_whitespace(client, auth_headers):
    created = client.post(
        "/api/v1/items/",
        headers=auth_headers,
        json={"name": "  Steel Blade  "},
    )
    assert created.status_code == 201
    assert created.json()["name"] == "Steel Blade"


def test_update_item(client, auth_headers):
    client.post("/api/v1/items/", headers=auth_headers, json={"name": "Draft", "strength": 5})
    response = client.put(
        "/api/v1/items/1",
        headers=auth_headers,
        json={"name": "Finished", "description": "Tempered", "strength": 70},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Finished"
    assert response.json()["strength"] == 70


def test_patch_item_updates_one_field(client, auth_headers):
    client.post(
        "/api/v1/items/",
        headers=auth_headers,
        json={"name": "Draft", "description": "Keep me", "strength": 5},
    )
    response = client.patch("/api/v1/items/1", headers=auth_headers, json={"strength": 40})
    assert response.status_code == 200
    assert response.json()["name"] == "Draft"
    assert response.json()["description"] == "Keep me"
    assert response.json()["strength"] == 40


def test_delete_item(client, auth_headers):
    client.post("/api/v1/items/", headers=auth_headers, json={"name": "Scrap"})
    deleted = client.delete("/api/v1/items/1", headers=auth_headers)
    assert deleted.status_code == 204

    missing = client.get("/api/v1/items/1")
    assert missing.status_code == 404
    assert missing.json()["detail"] == "Item not found"


def test_missing_item_returns_404(client):
    response = client.get("/api/v1/items/99")
    assert response.status_code == 404


def test_create_rejects_invalid_strength(client, auth_headers):
    response = client.post(
        "/api/v1/items/",
        headers=auth_headers,
        json={"name": "Broken", "strength": 0},
    )
    assert response.status_code == 422


def test_create_item_requires_auth(client):
    response = client.post("/api/v1/items/", json={"name": "Nope"})
    assert response.status_code == 401


def test_cannot_update_someone_elses_item(client, auth_headers, other_auth_headers):
    client.post("/api/v1/items/", headers=auth_headers, json={"name": "Mine"})
    response = client.put(
        "/api/v1/items/1",
        headers=other_auth_headers,
        json={"name": "Stolen", "strength": 10},
    )
    assert response.status_code == 403
