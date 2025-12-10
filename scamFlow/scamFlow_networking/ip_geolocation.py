import datetime
import requests
import json
import geopy

from geopy.geocoders import Nominatim

# Tool 1: For structured geocoding
geolocator = Nominatim(user_agent="scamFlow_detector")

# Tool 2: API fallback (ip-api.com - no key required for basic usage, limited to 45 requests per minute)
API_URL = "http://ip-api.com/json/"

def geolocate_ip(ip_address):
    """
    Geolocate an IP address using geopy and fallback to ip-api.com if necessary.
    
    Args:
        ip_address (str): The IP address to geolocate.
    Returns:
        dict: A dictionary containing geolocation data.
    """
    intel = {
        "ip": ip_address,
        "timestamp": datetime.datetime.isoformat(),
        "source": "ip_geolocation"
    }
    
    # First attempt: Use geopy (Nominatim)
    try:
        location = geolocator.geocode(ip_address)
        if location:
            intel.update({
                "geopy_latitude": location.latitude,
                "geopy_longitude": location.longitude,
                "geopy_address": location.address,
                "geopy_country": location.raw.get('country', 'N/A')
            })
        else:
            intel["geopy_status"] = "No data found"
    except Exception as e:
        intel["geopy_error"] = f"Getcode failed due to {str(e)}"
        
    # Backup attempt: Use ip-api.com with requests
    try:
        response = requests.get(f"{API_URL}{ip_address}", timeout=5)
        if response.status_code == 200:
            api_data = response.json()
            if api_data.get("status") == "success":
                intel.update({
                    "api_city": api_data.get("city", "N/A"),
                    "api_region": api_data.get("regionName", "N/A"),
                    "api_country": api_data.get("country", "N/A"),
                    "api_latitude": api_data.get("lat"),
                    "api_longitude": api_data.get("lon"),
                    "api_isp": api_data.get("isp", "N/A"),
                    "api_org": api_data.get("org", "N/A"),
                    "api_timezone": api_data.get("timezone", "N/A")
                })
            else:
                intel["ipapi_status"] = api_data.get("message", "No data found")
        else:
            intel["ipapi_error"] = f"HTTP error {response.status_code}"
    except Exception as e:
        intel["ipapi_error"] = f"Request failed due to {str(e)}"
    return intel

if __name__ == "__main__":
    ip = input("Enter an IP address to geolocate: ") or "8.8.8.8"
    result = geolocate_ip(ip)
    print(json.dumps(result, indent=4))