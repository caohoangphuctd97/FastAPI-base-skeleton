
from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health():
    response = client.get('/api/v1beta1/health')
    assert response.text == "Ok"
