"""
Tests use a fake model so they run without needing the real house_price.pkl
(which is large and version-pinned to a specific scikit-learn build). This
keeps CI fast and independent of the actual trained artifact -- the real
model is exercised manually via Swagger UI / the notebook's own sanity
check instead.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.inference import predictor


class _FakeModel:
    """Stands in for the real sklearn Pipeline: same .predict() interface."""

    def predict(self, X):
        return [4_200_000.0]


@pytest.fixture(autouse=True)
def fake_loaded_model():
    predictor._model = _FakeModel()
    yield
    predictor._model = None


client = TestClient(app)

VALID_PAYLOAD = {
    "location": "mumbai",
    "carpet_area_sqft": 1000,
    "floor_num": 3,
    "bathroom": 2,
    "balcony": 1,
    "furnishing": "Semi-Furnished",
    "transaction": "Resale",
    "ownership": "Freehold",
    "facing": "East",
}


def test_health_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_happy_path():
    response = client.post("/predict", json=VALID_PAYLOAD)
    assert response.status_code == 200
    body = response.json()
    assert "predicted_price" in body
    assert isinstance(body["predicted_price"], float)
    assert body["predicted_price"] == 4_200_000.0


def test_predict_invalid_input_missing_fields():
    # Missing required fields entirely -> 422 Unprocessable Entity
    response = client.post("/predict", json={"location": "mumbai"})
    assert response.status_code == 422


def test_predict_invalid_area_not_positive():
    payload = {**VALID_PAYLOAD, "carpet_area_sqft": 0}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
