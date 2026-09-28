import pytest
import requests

from api.objects_api import create_object, delete_object

@pytest.fixture(scope="session")
def api_client():
    with requests.Session() as session:
        yield session

@pytest.fixture
def created_object(api_client):
    payload = {
        "name": "QA Test Object",
        "data": {"year": 2026, "price": 999.99},
    }

    response = create_object(api_client, payload)
    assert response.status_code == 200, response.text

    obj = response.json()
    object_id = obj["id"]

    try:
        yield obj
    finally:
        delete_response = delete_object(api_client, object_id)
        assert delete_response.status_code in (200, 204), (
            f"Could not delete object {object_id}: "
            f"{delete_response.status_code} {delete_response.text}"
        )
