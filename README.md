# REST API Tests with Pytest

Automated tests for the authenticated [RESTful API](https://restful-api.dev/). The project covers reading objects, creating objects from JSON test data, updating them with PATCH, and checking the response for a nonexistent object.

## Tech stack

- Python
- pytest
- requests
- python-dotenv

## Setup

Run all commands from the project root. The examples below use Bash on Linux.

```bash
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Check that `.env` contains the API address:

```env
BASE_URL=https://api.restful-api.dev/collections/{collectionName}
```

## Run the tests

```bash
python -m pytest -v tests
```

To run only the object creation tests:

```bash
python -m pytest -v tests -k "create_object"
```

## Project structure

```text
api/               HTTP request functions
data/              JSON test cases
tests/             API test scenarios
utils/             JSON data loader
models/            Pydantic models
config.py          Environment configuration
conftest.py        Shared pytest fixtures
```

Tests that create objects remove them during cleanup. They make requests to an external service, so a network or service timeout can cause a run to fail even when the assertions are correct. See the pytest traceback for the affected request.

## Response Validation

API responses are validated with Pydantic v2 using nested models and `model_validate(..., strict=True)`. Validation checks that required fields are present and their values match the declared types.

Additional response fields are accepted and ignored by the models. The schema covers objects containing `year` and `price`; it is not intended to describe every object supported by the API.

Schema validation complements assertions that verify expected values and CRUD behavior. Objects created by the POST tests are cleaned up even when response validation or assertions fail, provided the response includes an object ID.

## Reporting and Diagnostics

The project uses **Allure Pytest** to document test execution and simplify failure analysis.

Reports include:

- Test grouping by feature and story, with severity labels for API scenarios.
- Named steps for requests, response validation, and cleanup.
- JSON request bodies and JSON or text response attachments.
- HTTP request details and response status codes for manual reproduction.

### Generate an Allure Report

Install the Python dependencies from `requirements.txt`. The **Allure Report 2 CLI** must be installed separately and available on `PATH`; it requires Java.

Run the tests and collect fresh results:

```bash
python -m pytest -v --alluredir=allure-results --clean-alluredir
```

Generate and open the HTML report:

```bash
allure generate allure-results -o allure-report --clean
allure open allure-report
```

Reports can also be generated after a failed test run. The `allure-results/` and `allure-report/` directories are excluded from version control.

## Test Isolation and Error Handling

API tests prepare their own objects through function-scoped fixtures and remove them during teardown. Tests use the IDs returned during setup rather than relying on data created by another test.

Successful object responses are validated against **Pydantic v2** models using `model_validate(..., strict=True)`. Separate assertions check field values and persisted changes.

Negative checks cover:

- Propagation of `Timeout` and `ConnectionError` from the API client's transport layer.
- A `404` response for a nonexistent object and the `HTTPError` raised by `raise_for_status()`.
- Rejection of invalid response data by Pydantic models.

Transport exceptions are simulated with `monkeypatch`; these tests do not send network requests. CRUD tests exercise the real API.

### Check Test Order Independence

Run tests in a reproducible shuffled order:

```bash
python -m pytest tests/test_objects.py -v --randomly-seed=137 --randomly-dont-reset-seed
```

Keep the seed, test selection, and environment when investigating an order-dependent failure.

### Reproduce a Request

Use the method, URL, relevant headers, and request body recorded in Allure to reconstruct a request in curl. Supply authentication credentials locally.

Compare the returned status and body with the report. Reproduction may require recreating test data because fixture teardown removes temporary objects.
