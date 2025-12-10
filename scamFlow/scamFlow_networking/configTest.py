# tests/conftest.py
import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_geopy_success(monkeypatch):
    mock_location = Mock()
    mock_location.address = "1600 Pennsylvania Ave NW, Washington, DC"
    mock_location.latitude = 38.8977
    mock_location.longitude = -77.0365
    mock_location.raw = {"address": {"country": "United States"}}

    def fake_geocode(ip):
        return mock_location if ip in ["8.8.8.8", "1.1.1.1"] else None

    monkeypatch.setattr("scamFlow_networking.ip_geolocation.geolocator.geocode", fake_geocode)

@pytest.fixture
def mock_ip_api_success(responses):
    responses.add(
        responses.GET,
        "http://ip-api.com/json/8.8.8.8",
        json={
            "status": "success",
            "country": "United States",
            "regionName": "California",
            "city": "Mountain View",
            "isp": "Google LLC",
            "org": "Google",
            "lat": 37.4056,
            "lon": -122.0775,
            "timezone": "America/Los_Angeles"
        },
        status=200
    )
    responses.add(
        responses.GET,
        "http://ip-api.com/json/1.1.1.1",
        json={
            "status": "success",
            "country": "Australia",
            "city": "Sydney",
            "isp": "Cloudflare",
            "org": "APNIC",
            "lat": -33.869,
            "lon": 151.206,
            "timezone": "Australia/Sydney"
        },
        status=200
    )
