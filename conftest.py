import pytest
import requests
import allure

from config import BASE_URL, X_API_KEY
from api.objects_api import ObjectsApiClient
from helpers.allure_helpers import attach_response, attach_json
from helpers.assertions import assert_status_code
from models.object_response import ObjectResponse


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
@allure.title("Prepare and clean up an API object")
def created_object(objects_client):
    payload = {
        "name": "QA Test Object",
        "data": {"year": 2026, "price": 999.99},
    }

    with allure.step("Send a request to create an object"):
        attach_json(payload, "Request body")
        response = objects_client.create_object(payload)
        attach_response(response)
    assert_status_code(response, 200)

    with allure.step("Get the created object ID"):
        obj = response.json()
        object_id = obj["id"]

    try:
        with allure.step("Validate the response schema"):
            object_created = ObjectResponse.model_validate(obj, strict=True)
        
        with allure.step("Check that created object matches the request"):
            assert object_created.name == payload["name"]
            assert object_created.data.model_dump() == payload["data"]
        yield object_created
    finally:
        with allure.step("Delete the created object"):
            delete_response = objects_client.delete_object(object_id)
            attach_response(delete_response)
            assert delete_response.status_code in (200, 204), (
                f"Could not delete object {object_id}: "
                f"{delete_response.status_code} {delete_response.text}"
            )
