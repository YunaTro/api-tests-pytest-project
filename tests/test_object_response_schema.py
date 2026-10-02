from copy import deepcopy

import pytest
import allure
from pydantic import ValidationError

from models.object_response import ObjectResponse
from helpers.allure_helpers import attach_json

VALID_RESPONSE = {
    "id": "7",
    "name": "QA Phone",
    "data": {
      "year": 2025,
      "price": 599.50
    }
}

@allure.feature("Response models")
@allure.story("Object response validation")
@allure.title("Object schema rejects invalid nested data")
@pytest.mark.parametrize(
    "field_name, invalid_value",
    [
        pytest.param("year", "2026", id="year-as-string"),
        pytest.param("year", None, id="year-is-null"),
        pytest.param("price", "unknown", id="price-as-text"),
        pytest.param("price", None, id="price-is-null"),
    ],
)
def test_object_schema_rejects_invalid_nested_data(field_name, invalid_value):
    response_data = deepcopy(VALID_RESPONSE)
    response_data["data"][field_name] = invalid_value

    attach_json(response_data, "Input to schema validation")

    with allure.step("Check that invalid data is rejected"):
        with pytest.raises(ValidationError) as exc_info:
            ObjectResponse.model_validate(response_data, strict=True)

        error_locations = [error["loc"] for error in exc_info.value.errors()]
        assert ("data", field_name) in error_locations


@allure.feature("Response models")
@allure.story("Object response validation")
@allure.title("Object schema rejects invalid data")
@pytest.mark.parametrize(
    "field_name, invalid_value",
    [
        pytest.param("id", 7, id="id-as-integer"),
        pytest.param("data", None, id="data-is-null"),
        pytest.param("name", None, id="name-is-null"),
    ],
)
def test_object_schema_rejects_invalid_data(field_name, invalid_value):
    response_data = deepcopy(VALID_RESPONSE)
    response_data[field_name] = invalid_value

    attach_json(response_data, "Input to schema validation")

    with allure.step("Check that invalid data is rejected"):
        with pytest.raises(ValidationError) as exc_info:
            ObjectResponse.model_validate(response_data, strict=True)

        error_locations = [error["loc"] for error in exc_info.value.errors()]
        assert (field_name,) in error_locations


@allure.feature("Response models")
@allure.story("Object response validation")
@allure.title("Object schema requires id")
def test_object_schema_requires_id():
    response_data = deepcopy(VALID_RESPONSE)
    del response_data["id"]

    attach_json(response_data, "Input to schema validation")

    with allure.step("Check that invalid data is rejected"):
        with pytest.raises(ValidationError) as exc_info:
            ObjectResponse.model_validate(response_data, strict=True)
        error_locations = [error["loc"] for error in exc_info.value.errors()]
        assert ("id",) in error_locations

@allure.feature("Response models")
@allure.story("Object response validation")
@allure.title("Object schema accepts added fields such as created_at")
def test_object_schema_accepts_created_at():
    response_data = deepcopy(VALID_RESPONSE)
    response_data["createdAt"] = "2026.04.05T12:03"

    attach_json(response_data, "Input to schema validation")

    with allure.step("Check that valid data is accepted"):
        ObjectResponse.model_validate(response_data, strict=True)
