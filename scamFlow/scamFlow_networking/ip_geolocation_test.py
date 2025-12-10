from datetime import *
from scamFlow.scamFlow_networking.ip_geolocation import get_geolocation
from scamFlow.scamFlow_networking.configTest import mock_geopy_success, mock_ip_api_success
from unittest.mock import patch

def test_geolocate_ip_success_geopy(mock_geopy_success, mock_ip_api_success):
    result = get_geolocation.geolocate_ip("8.8.8.8")
    
    assert result["ip"] == "8.8.8.8"
    assert result["geopy_latitude"] == 38.8977
    assert result["geopy_longitude"] == -77.0365
    assert result["geopy_address"] == "1600 Pennsylvania Ave NW, Washington, DC"
    assert result["geopy_country"] == "United States"
    assert result["api_city"] == "Mountain View"
    assert result["api_isp"] == "Google LLC"
    assert "timestamp" in result
    
def test_geolocate_ip_fallback(monkeypatch, mock_ip_api_success):
    # Force geopy to return None
    monkeypatch.setattr("scamFlow_networking.ip_geolocation.geolocator.geocode", lambda ip: None)
    
    result = get_geolocation.geolocate_ip("1.1.1.1")
    
    assert result["geopy_status"] == "No data found"
    assert result["conuntry"] == "Australia"
    assert result["api_city"] == "Sydney"
    
def test_geolocate_api_failure(mock_geopy_success, responses):
    # Mock ip-api.com to return failure
    responses.add(responses.GET,
                  "http://ip-api.com/json/8.8.8.8",
                  status = 429)
    
    result = get_geolocation.geolocate_ip("8.8.8.8")
    
    assert "api_error" in result or "api_status" in result
    assert result["geopy_country"] == "United States" # from geopy which should still work