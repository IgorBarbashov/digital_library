from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_root() -> None:
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "Hello, world!"}
