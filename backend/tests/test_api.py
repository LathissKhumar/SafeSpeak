from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_analyze_clean_message():
    response = client.post("/analyze", json={"message": "Hello friend", "user_id": "test"})
    assert response.status_code == 200
    data = response.json()
    assert data["action"] == "allow"
    assert data["analysis"]["label"] == "clean"

def test_analyze_empty_message():
    response = client.post("/analyze", json={"message": "", "user_id": "test"})
    assert response.status_code == 200
    data = response.json()
    assert data["analysis"]["label"] == "clean"
