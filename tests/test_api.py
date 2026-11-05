from fastapi.testclient import TestClient

from safesignal.api import app
from safesignal.generate import demo

client = TestClient(app)


def test_health():
    assert client.get("/health").json()["status"] == "ok"


def test_ingest_endpoint():
    response = client.post("/ingest", json=demo())
    assert response.status_code == 200
    data = response.json()
    assert data["alerts"]
    assert data["digests"]
    assert any(alert["category"] == "self_harm" for alert in data["alerts"])
