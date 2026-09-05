import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.repositories import items as items_repository


@pytest.fixture()
def client():
    items_repository.reset()
    with TestClient(app) as test_client:
        yield test_client
