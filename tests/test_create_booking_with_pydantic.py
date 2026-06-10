import allure
import requests
import pytest
from pydantic import ValidationError

from conftest import api_client
from core.models.booking import BookingResponse


@allure.feature("Test create booking with pydantic")
@allure.story("Positive create booking with custom data")
def test_create_booking_with_pydantic(api_client):
    booking_data = {
    "firstname": "Petr",
    "lastname": "Petrov",
    "totalprice": 222,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2025-06-05",
        "checkout": "2025-06-06"
    },
    "additionalneeds": "Full board"
    }

    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed {e}")
    assert response["booking"]["firstname"] == booking_data["firstname"]
    assert response["booking"]["lastname"] == booking_data["lastname"]
    assert response["booking"]["totalprice"] == booking_data["totalprice"]
    assert response["booking"]["depositpaid"] == booking_data["depositpaid"]
    assert response["booking"]["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"]
    assert response["booking"]["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"]


@allure.feature("Test create booking")
@allure.story("Test method not allowed")
def test_create_booking_method_not_allowed(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 405
    mocker.patch.object(api_client.session, "post", return_value = mock_response)
    with pytest.raises(AssertionError, match = f"Expected status_code 200 but got 405"):
        api_client.create_booking(booking_data = {})


@allure.feature("Test create booking")
@allure.story("Page not found")
def test_create_booking_not_found(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404
    mocker.patch.object(api_client.session, "post", return_value = mock_response)
    with pytest.raises(AssertionError, match = f"Expected status_code 200 but got 404"):
        api_client.create_booking(booking_data = {})


@allure.feature("Test create booking")
@allure.story("Unprocessable Entity")
def test_create_booking_unprocessable_entity(api_client, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 422
    mocker.patch.object(api_client.session, "post", return_value = mock_response)
    with pytest.raises(AssertionError, match = f"Expected status_code 200 but got 422"):
        api_client.create_booking(booking_data = {})


@allure.feature("Test create booking")
@allure.story("Test timeouts")
def test_create_booking_test_timeouts(api_client, mocker):
    mocker.patch.object(api_client.session, "post", side_effect = requests.Timeout)
    with pytest.raises(requests.Timeout):
        api_client.create_booking(booking_data = {})


@allure.feature("Test create booking")
@allure.story("Test server unavailability")
def test_create_booking_server_unavailability(api_client, mocker):
    mocker.patch.object(api_client.session, "post", side_effect = Exception("Server unavailable"))
    with pytest.raises(Exception, match= "Server unavailable"):
        api_client.create_booking(booking_data = {})


@allure.feature("Test create booking")
@allure.story("Test internal server error")
def test_create_booking_internal_server_error(api_client,mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 500
    mocker.patch.object(api_client.session, "post", return_value = mock_response)


@allure.feature("Test create booking")
@allure.story("Positive create booking with random data")
def test_create_booking_with_random_data(api_client,booking_dates):
    booking_data = {
        "firstname": "Petr",
        "lastname": "Petrov",
        "totalprice": 222,
        "depositpaid": True,
        "bookingdates" : booking_dates,
        "additionalneeds": "Full board"
    }
    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed {e}")
    assert response["booking"]["firstname"] == booking_data["firstname"]
    assert response["booking"]["lastname"] == booking_data["lastname"]
    assert response["booking"]["totalprice"] == booking_data["totalprice"]
    assert response["booking"]["depositpaid"] == booking_data["depositpaid"]
    assert response["booking"]["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"]
    assert response["booking"]["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"]


@allure.feature("Test create booking")
@allure.story("Negative create booking: checkin=checkout")
def test_create_booking_checkin_checkout_equal(api_client):
    booking_data = {
    "firstname": "Petr",
    "lastname": "Petrov",
    "totalprice": 222,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2025-06-05",
        "checkout": "2025-06-05"
    },
    "additionalneeds": "Full board"
    }

    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed {e}")
    assert response["booking"]["firstname"] == booking_data["firstname"]
    assert response["booking"]["lastname"] == booking_data["lastname"]
    assert response["booking"]["totalprice"] == booking_data["totalprice"]
    assert response["booking"]["depositpaid"] == booking_data["depositpaid"]
    assert response["booking"]["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"]
    assert response["booking"]["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"]


@allure.feature("Test create booking")
@allure.story("Negative create booking: checkin>checkout")
def test_create_booking_checkin_later_than_checkout(api_client):
    booking_data = {
    "firstname": "Petr",
    "lastname": "Petrov",
    "totalprice": 222,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2025-06-09",
        "checkout": "2025-06-05"
    },
    "additionalneeds": "Full board"
    }

    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed {e}")
    assert response["booking"]["firstname"] == booking_data["firstname"]
    assert response["booking"]["lastname"] == booking_data["lastname"]
    assert response["booking"]["totalprice"] == booking_data["totalprice"]
    assert response["booking"]["depositpaid"] == booking_data["depositpaid"]
    assert response["booking"]["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"]
    assert response["booking"]["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"]


@allure.feature("Test create booking")
@allure.story("Positive create booking with random booking data")
def test_create_booking_with_random_booking_data(api_client, generate_random_booking_data):
    booking_data = generate_random_booking_data

    response = api_client.create_booking(booking_data)
    try:
        BookingResponse(**response)
    except ValidationError as e:
        raise ValidationError(f"Response validation failed {e}")
    assert response["booking"]["firstname"] == booking_data["firstname"]
    assert response["booking"]["lastname"] == booking_data["lastname"]
    assert response["booking"]["totalprice"] == booking_data["totalprice"]
    assert response["booking"]["depositpaid"] == booking_data["depositpaid"]
    assert response["booking"]["bookingdates"]["checkin"] == booking_data["bookingdates"]["checkin"]
    assert response["booking"]["bookingdates"]["checkout"] == booking_data["bookingdates"]["checkout"]