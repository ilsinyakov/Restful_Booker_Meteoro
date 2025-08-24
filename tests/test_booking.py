from typing import Any

import allure
import pytest
import requests

from config import BASE_URL, USERNAME
from schemas.booking import BookingSchema, CreateBookingSchema
from util.allure_attach import attach_request_response


@allure.feature("Booking Management")
class TestPositive:

    @allure.title("Create new booking")
    @allure.story("Positive")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.positive
    def test_create_booking(self, api_client: requests.Session, valid_booking: dict[str, Any]) -> int:  # noqa: PLR6301
        with allure.step("Send booking creation request"):
            response = api_client.post(f"{BASE_URL}/booking", json=valid_booking)
            attach_request_response(response)

        with allure.step("Verify response code and schema"):
            assert response.status_code == requests.codes.ok
            booking = response.json()
            CreateBookingSchema(**booking)

        return booking["bookingid"]

    @allure.title("Get booking details")
    @allure.story("Positive")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    def test_get_booking(self, api_client: requests.Session, valid_booking: dict[str, Any]) -> None:
        booking_id = self.test_create_booking(api_client, valid_booking)

        with allure.step(f"Get booking by ID: {booking_id}"):
            response = api_client.get(f"{BASE_URL}/booking/{booking_id}")
            attach_request_response(response)

        with allure.step("Verify response code and schema"):
            assert response.status_code == requests.codes.ok
            BookingSchema(**response.json())

    @allure.title("Update booking details")
    @allure.story("Positive")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    def test_update_booking(
        self,
        api_client: requests.Session,
        valid_booking: dict[str, Any],
        auth_token: str,
    ) -> None:
        booking_id = self.test_create_booking(api_client, valid_booking)
        updated_data = valid_booking.copy()
        updated_data["firstname"] = "UpdatedName"

        with allure.step("Send booking update request"):
            headers = {"Cookie": f"token={auth_token}"}
            response = api_client.put(
                f"{BASE_URL}/booking/{booking_id}",
                json=updated_data,
                headers=headers,
            )
            attach_request_response(response)

        with allure.step("Verify response code and schema"):
            assert response.status_code == requests.codes.ok
            BookingSchema(**response.json())

        with allure.step("Verify updated firstname"):
            assert response.json()["firstname"] == "UpdatedName"

    @allure.title("Delete booking")
    @allure.story("Positive")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    def test_delete_booking(
        self,
        api_client: requests.Session,
        valid_booking: dict[str, Any],
        auth_token: str,
    ) -> None:
        booking_id = self.test_create_booking(api_client, valid_booking)

        with allure.step("Send booking deletion request"):
            headers = {"Cookie": f"token={auth_token}"}
            response = api_client.delete(
                f"{BASE_URL}/booking/{booking_id}",
                headers=headers,
            )
            attach_request_response(response)

        with allure.step("Verify response code"):
            assert response.status_code == requests.codes.created

        with allure.step("Try get deleted booking"):
            response = api_client.get(f"{BASE_URL}/booking/{booking_id}")
            attach_request_response(response)
            assert response.status_code == requests.codes.not_found


@allure.feature("Booking Management")
class TestNegative:

    @allure.title("Create booking with invalid data")
    @allure.story("Negative")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    @pytest.mark.xfail(reason="Actual response code is 500, expected - 400")
    def test_create_invalid_booking(self, api_client: requests.Session) -> None:  # noqa: PLR6301
        with allure.step("Send invalid booking creation request"):
            response = api_client.post(f"{BASE_URL}/booking", json={})
            attach_request_response(response)

        with allure.step("Verify bad request response"):
            assert response.status_code == requests.codes.bad_request

    @allure.title("Get non-existent booking")
    @allure.story("Negative")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    def test_get_nonexistent_booking(self, api_client: requests.Session) -> None:  # noqa: PLR6301
        with allure.step("Request non-existent booking"):
            response = api_client.get(f"{BASE_URL}/booking/999999")
            attach_request_response(response)

        with allure.step("Verify not found response"):
            assert response.status_code == requests.codes.not_found

    @allure.title("Update booking without token")
    @allure.story("Negative")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    def test_update_without_token(  # noqa: PLR6301
        self,
        api_client: requests.Session,
        valid_booking: dict[str, Any],
    ) -> None:
        booking_id = TestPositive().test_create_booking(api_client, valid_booking)

        with allure.step("Attempt update without authentication"):
            response = api_client.put(
                f"{BASE_URL}/booking/{booking_id}",
                json=valid_booking,
            )
            attach_request_response(response)

        with allure.step("Verify forbidden response"):
            assert response.status_code == requests.codes.forbidden

    @allure.title("Delete booking without token")
    @allure.story("Negative")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    def test_delete_without_token(  # noqa: PLR6301
        self,
        api_client: requests.Session,
        valid_booking: dict[str, Any],
    ) -> None:
        booking_id = TestPositive().test_create_booking(api_client, valid_booking)

        with allure.step("Attempt deletion without authentication"):
            response = api_client.delete(f"{BASE_URL}/booking/{booking_id}")
            attach_request_response(response)

        with allure.step("Verify forbidden response"):
            assert response.status_code == requests.codes.forbidden

    @allure.title("Authorization with invalid password")
    @allure.story("Negative")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.negative
    def test_auth_invalid_password(self, api_client: requests.Session) -> None:  # noqa: PLR6301
        invalid_credentials = {
            "username": USERNAME,
            "password": "wrongpassword",
        }

        with allure.step("Send auth request with invalid password"):
            response = api_client.post(f"{BASE_URL}/auth", json=invalid_credentials)
            attach_request_response(response)

        with allure.step("Verify authentication failure"):
            assert response.status_code == requests.codes.ok
            assert "reason" in response.json()
            assert response.json()["reason"] == "Bad credentials"
