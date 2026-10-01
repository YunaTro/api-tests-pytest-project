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
pytest -v tests
```

To run only the object creation tests:

```bash
pytest -v tests -k "create_object"
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
