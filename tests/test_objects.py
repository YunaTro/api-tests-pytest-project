import pytest

from api.objects_api import create_object, get_object, update_object, delete_object
from utils.data_loader import load_json

def test_update_object_name(api_client, objects_client, created_object):
    object_id = created_object["id"]
    new_name = "Updated QA Object"

    response = update_object(
        api_client,
        object_id,
        {"name": new_name},
    )

    assert response.status_code == 200, response.text
    assert response.json()["name"] == new_name

    get_response = objects_client.get_object(object_id)
    assert get_response.status_code == 200
    assert get_response.json()["name"] == new_name


objects = load_json("data/objects.json")

@pytest.mark.parametrize("payload", objects)
def test_create_object(api_client, payload):
    response = create_object(api_client, payload)
    assert response.status_code == 200, response.text

    created_object = response.json()
    object_id = created_object.get("id")
    assert object_id, f"Response has no object ID: {created_object}"

    try:
        assert created_object["name"] == payload["name"]
        assert created_object["data"] == payload["data"]
    finally:
        delete_response = delete_object(api_client, object_id)
        assert delete_response.status_code in (200, 204), (
            f"Could not delete object {object_id}: "
            f"{delete_response.status_code} {delete_response.text}"
        )

def test_get_nonexistent_object(api_client):
    response = get_object(api_client, "qa-object-that-does-not-exist-999999")

    assert response.status_code == 404, (
        f"Expected 404, got {response.status_code}"
    )
