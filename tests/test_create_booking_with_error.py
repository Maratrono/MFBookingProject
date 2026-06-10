import allure
import requests
import pytest
from requests.cookies import MockResponse

@allure.feature("Test create booking")
@allure.story("Test server error")
def test_create_booking_internal_server_error(api_client):
    payload = {
    "firstname" : "Jim",
    "totalprice" : 111,
    "depositpaid" : True,
    "bookingdates" : {
        "checkin" : "2018-01-01",
        "checkout" : "2019-01-01"
    },
    "additionalneeds" : "Breakfast"
    }
    response = api_client.create_booking_with_error(payload)
    assert response.status_code == 500


