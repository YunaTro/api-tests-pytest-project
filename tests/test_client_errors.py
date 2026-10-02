import allure
import pytest
import requests
from requests.exceptions import Timeout, ConnectionError

from api.base_api_client import BaseApiClient


@allure.feature("API client")
@allure.story("Transport errors")
@allure.title("API client propagates transport errors")
@pytest.mark.parametrize(
    "exception_class, error_message",
    [
        pytest.param(Timeout, "Request timed out", id="timeout"),
        pytest.param(ConnectionError, "Connection error", id="connection-error"),
    ]
)
def test_request_propagates_transport_error(monkeypatch, exception_class, error_message):
    def failing_request(method, url, **kwargs):
        raise exception_class(error_message)

    with requests.Session() as session:
        monkeypatch.setattr(session, "request", failing_request)

        client = BaseApiClient(
            session=session,
            base_url="https://api.example.com",
        )

        with allure.step(f"Check that {exception_class.__name__} reaches the caller"):
            with pytest.raises(exception_class, match=error_message):
                client.request("GET", "/objects/7")