import pytest
import allure

from requests.exceptions import HTTPError

from models.object_response import ObjectResponse
from utils.data_loader import load_json

from helpers.allure_helpers import attach_json, attach_response
from helpers.assertions import assert_status_code

@allure.feature("Objects API")
@allure.story("Update object")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Updated object contains patched data")
def test_update_object_name(objects_client, created_object):
    object_id = created_object.id
    with allure.step("Send request to update object"):
        new_name = "Updated QA Object"
        payload = {"name": new_name}
        attach_json(payload, "Request Body")
        response = objects_client.update_object(object_id, payload)
        attach_response(response)

    assert_status_code(response, 200)

    with allure.step("Validate the update response schema"):
        obj = ObjectResponse.model_validate(response.json(), strict=True)
    
    with allure.step("Check updated name and unchanged fields"):
        assert obj.id == object_id
        assert obj.name == new_name
        assert obj.data.model_dump() == created_object.data.model_dump()

    with allure.step("Send request to get the updated object"):
        get_response = objects_client.get_object(object_id)
        attach_response(get_response)

    assert_status_code(get_response, 200)

    with allure.step("Validate the get response schema"):
        get_obj = ObjectResponse.model_validate(get_response.json(), strict=True)
    
    with allure.step("Check that the update was persisted"):
        assert get_obj.id == object_id
        assert get_obj.name == new_name
        assert get_obj.data.model_dump() == created_object.data.model_dump()


objects = load_json("data/objects.json")

@allure.feature("Objects API")
@allure.story("Create object")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Created object contains the submitted data") 
@pytest.mark.parametrize("payload", objects)
def test_create_object(objects_client, payload):
    with allure.step("Send request to create an object"):
        attach_json(payload, "Request body")
        response = objects_client.create_object(payload)
        attach_response(response)
    assert_status_code(response, 200)

    with allure.step("Read the created object ID"):
        response_data = response.json()
        object_id = response_data["id"]

    try:
        with allure.step("Validate the response schema"):
            created_object = ObjectResponse.model_validate(response_data, strict=True)

        with allure.step("Check that created object matches the request"):
            assert created_object.name == payload["name"]
            assert created_object.data.model_dump() == payload["data"]
    finally:
        if object_id is not None:
            with allure.step("Delete the created object"):
                delete_response = objects_client.delete_object(object_id)
                attach_response(delete_response)
                assert delete_response.status_code in (200, 204), (
                    f"Could not delete object {object_id}: "
                    f"{delete_response.status_code} {delete_response.text}"
                )

@allure.feature("Objects API")
@allure.story("Read object")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Nonexistent object can not be found")
def test_get_nonexistent_object(objects_client):
    with allure.step("Get nonexistent object"):
        response = objects_client.get_object("qa-object-that-does-not-exist-999999")
        attach_response(response)

    assert_status_code(response, 404)

    with allure.step("Check that an error response raises HTTPError"):
        with pytest.raises(HTTPError) as exc_info:
            response.raise_for_status()

        assert exc_info.value.response is response

@allure.feature("Objects API")
@allure.story("Read object")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Created object can be retrieved by ID")
def test_get_created_object(objects_client, created_object):
    with allure.step("Get the object by ID"):
        response = objects_client.get_object(created_object.id)
        attach_response(response)

    assert_status_code(response, 200)

    with allure.step("Validate the GET response schema"):
        fetched_object = ObjectResponse.model_validate(response.json(), strict=True)

    with allure.step("Check that retrieved data matches the created object"):
        assert fetched_object.id == created_object.id
        assert fetched_object.name == created_object.name
        assert fetched_object.data.model_dump() == created_object.data.model_dump()