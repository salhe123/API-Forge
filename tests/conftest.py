import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import get_db
from app.db.base import Base
from app.main import create_app
from app.models.item import ItemModel  # noqa: F401
from app.models.user import UserModel  # noqa: F401


@pytest.fixture()
def client():
    application = create_app(testing=True)
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    application.dependency_overrides[get_db] = override_get_db
    with TestClient(application) as test_client:
        yield test_client
    application.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def auth_headers_for(client: TestClient, email: str, password: str = "secret123"):
    client.post("/api/v1/auth/register", json={"email": email, "password": password})
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    token = response.json()["access_token"]
    return {"Authorization": "Bearer {0}".format(token)}


@pytest.fixture()
def auth_headers(client):
    return auth_headers_for(client, "forge@example.com")


@pytest.fixture()
def other_auth_headers(client):
    return auth_headers_for(client, "other@example.com")
