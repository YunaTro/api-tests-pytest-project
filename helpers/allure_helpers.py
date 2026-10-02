import json

import allure
from requests.exceptions import JSONDecodeError


def attach_json(data, name):
    allure.attach(
        json.dumps(data, ensure_ascii=False, indent=2),
        name=name,
        attachment_type=allure.attachment_type.JSON,
    )


def attach_response(response):
    attach_http_details(response)
    try:
        body = response.json()
    except JSONDecodeError:
        allure.attach(
            response.text,
            name="Response body",
            attachment_type=allure.attachment_type.TEXT,
        )
    else:
        attach_json(body, "Response body")


def attach_http_details(response):
    request = response.request

    headers = {
        name: value
        for name, value in request.headers.items()
        if name.lower() in {"accept", "content-type"}
    }

    if "x-api-key" in request.headers:
        headers["x-api-key"] = "<REDACTED>"

    if "Authorization" in request.headers:
        headers["Authorization"] = "<REDACTED>"

    attach_json(
        {
            "method": request.method,
            "url": request.url,
            "headers": headers,
            "response_status": response.status_code,
        },
        "HTTP details",
    )