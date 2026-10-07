import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_index(client):
    """Test the root endpoint returns expected JSON and correct version"""
    rv = client.get("/")
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data["service"] == "checkout-api"
    assert json_data["version"] == "v2.4"
    assert json_data["message"] == "Release Readiness Demo"

def test_health(client):
    """Test the health check endpoint returns 200 and healthy checks"""
    rv = client.get("/health")
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data["status"] == "healthy"
    assert "checks" in json_data
    assert "database" in json_data["checks"]
    assert "redis" in json_data["checks"]

def test_health_does_not_claim_dependencies_are_connected(client, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://configured")
    monkeypatch.setenv("REDIS_URL", "redis://configured")

    rv = client.get("/health")

    assert rv.status_code == 200
    assert rv.get_json()["checks"] == {
        "database": "configured",
        "redis": "configured",
    }

def test_readiness_requires_dependency_configuration(client, monkeypatch):
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("REDIS_URL", raising=False)

    rv = client.get("/ready")

    assert rv.status_code == 503
    assert rv.get_json()["status"] == "not_ready"

def test_readiness_passes_with_dependency_configuration(client, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql://configured")
    monkeypatch.setenv("REDIS_URL", "redis://configured")

    rv = client.get("/ready")

    assert rv.status_code == 200
    assert rv.get_json()["status"] == "ready"
