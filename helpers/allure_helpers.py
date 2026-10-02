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