import pytest
import requests

from config import BASE_URL, X_API_KEY
from api.objects_api import ObjectsApiClient

@pytest.fixture
def api_client():
    with requests.Session() as session:
        session.headers.update({
            "x-api-key": X_API_KEY
        })
        yield session

@pytest.fixture
def objects_client(api_client):
    return ObjectsApiClient(api_client, BASE_URL, timeout=(10, 25))

@pytest.fixture
def created_object(objects_client):
    payload = {
        "name": "QA Test Object",
        "data": {"year": 2026, "price": 999.99},
    }

    response = objects_client.create_object(payload)
    assert response.status_code == 200, response.text

    obj = response.json()
    object_id = obj["id"]

    try:
        yield obj
    finally:
        delete_response = objects_client.delete_object(object_id)
        assert delete_response.status_code in (200, 204), (
            f"Could not delete object {object_id}: "
            f"{delete_response.status_code} {delete_response.text}"
        )
