import pytest

from models.object_response import ObjectResponse
from utils.data_loader import load_json

def test_update_object_name(objects_client, created_object):
    object_id = created_object["id"]
    new_name = "Updated QA Object"

    response = objects_client.update_object(
        object_id,
        {"name": new_name},
    )

    assert response.status_code == 200, response.text
    obj = ObjectResponse.model_validate(response.json(), strict=True)
    assert obj.name == new_name

    get_response = objects_client.get_object(object_id)
    assert get_response.status_code == 200
    get_obj = ObjectResponse.model_validate(get_response.json(), strict=True)
    assert get_obj.name == new_name


objects = load_json("data/objects.json")

@pytest.mark.parametrize("payload", objects)
def test_create_object(objects_client, payload):
    response = objects_client.create_object(payload)
    assert response.status_code == 200, response.text

    response_data = response.json()
    object_id = response_data["id"]

    try:
        created_object = ObjectResponse.model_validate(response_data, strict=True)
        assert created_object.name == payload["name"]
        assert created_object.data.model_dump() == payload["data"]
    finally:
        delete_response = objects_client.delete_object(object_id)
        assert delete_response.status_code in (200, 204), (
            f"Could not delete object {object_id}: "
            f"{delete_response.status_code} {delete_response.text}"
        )

def test_get_nonexistent_object(objects_client):
    response = objects_client.get_object("qa-object-that-does-not-exist-999999")

    assert response.status_code == 404, (
        f"Expected 404, got {response.status_code}"
    )
