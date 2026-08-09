import allure
import requests
import jsonschema
import pytest
from schemas.booking_schemas import BOOKING_SCHEMA

from pydantic import ValidationError
from conftest import api_client
from core.models.booking import BookingResponse


@allure.feature("Test create booking")
def test_create_booking(api_client):
    payload = {
    "firstname" : "Jim",
    "lastname" : "Brown",
    "totalprice" : 111,
    "depositpaid" : True,
    "bookingdates" : {
        "checkin" : "2018-01-01",
        "checkout" : "2019-01-01"
    },
    "additionalneeds" : "Breakfast"
    }
    response_json = api_client.create_booking(payload)
    jsonschema.validate(response_json, BOOKING_SCHEMA)
    assert response_json["booking"]["firstname"] == payload["firstname"]
    assert response_json["booking"]["lastname"] == payload["lastname"]
    assert response_json["booking"]["totalprice"] == payload["totalprice"]
    assert response_json["booking"]["depositpaid"] == payload["depositpaid"]
    assert response_json["booking"]["bookingdates"]["checkin"] == payload["bookingdates"]["checkin"]
    assert response_json["booking"]["bookingdates"]["checkout"] == payload["bookingdates"]["checkout"]


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
@allure.story("Test server error")
def test_create_booking_internal_server_error(api_client):
    booking_data = {
    "firstname" : "Jim",
    "totalprice" : 111,
    "depositpaid" : True,
    "bookingdates" : {
        "checkin" : "2018-01-01",
        "checkout" : "2019-01-01"
    },
    "additionalneeds" : "Breakfast"
    }
    with pytest.raises(Exception, match="500 Server Error"):
        response = api_client.create_booking(booking_data)

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
    "firstname": "Ivan",
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



