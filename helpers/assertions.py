import allure

@allure.step("Check response status: expected {expected_status}")
def assert_status_code(response, expected_status):
    assert response.status_code == expected_status, (
        f"Expected status {expected_status}, "
        f"got {response.status_code}. "
        f"Response body: {response.text}"
    )