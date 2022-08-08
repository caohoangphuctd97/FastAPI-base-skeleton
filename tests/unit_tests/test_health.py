
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health():
    response = client.get('/health')
    assert response.text == "Ok"
