import allure
import requests
import jsonschema
from schemas.booking_schemas import BOOKING_SCHEMA


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








