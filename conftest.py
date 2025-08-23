from typing import Any

import pytest
import requests
from faker import Faker

from config import BASE_URL, PASSWORD, USERNAME


@pytest.fixture
def api_client() -> requests.Session:
    return requests.Session()


@pytest.fixture
def valid_booking() -> dict[str, Any]:
    fake = Faker()
    return {
        "firstname": fake.first_name(),
        "lastname": fake.last_name(),
        "totalprice": fake.random_int(min=100, max=1000),
        "depositpaid": fake.boolean(),
        "bookingdates": {
            "checkin": fake.date_between(start_date="-1y", end_date="today").isoformat(),
            "checkout": fake.date_between(start_date="today", end_date="+1y").isoformat(),
        },
        "additionalneeds": fake.sentence(),
    }


@pytest.fixture
def auth_token(api_client: requests.Session) -> str:
    credentials = {
        "username": USERNAME,
        "password": PASSWORD,
    }
    response = api_client.post(f"{BASE_URL}/auth", json=credentials)
    return response.json()["token"]
