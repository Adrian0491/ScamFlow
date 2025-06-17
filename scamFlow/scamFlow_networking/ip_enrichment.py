import threading
import requests
import json

from typing import Dict, Optional

# JSON Output main directory as a global variable
JSON_DIR = "scamFlow/JSON_Output"

class IPEnricher:
    """
        A utility class to enrich IP address metadata using the ip-api.com service.

        It retrieves geolocation, ISP, organization, and ASN information for a given IP address,
                 which can assist in identifying infrastructure used in scam or phishing emails.
    """

    def __init__(self, ip_address: str):
        self.ip_address = ip_address
        self.data: Dict[str, Optional[str]] = {}

    def enrich_ip(self) -> Dict[str, Optional[str]]:
        try:
            response = requests.get(f"http://ip-api.com/json/{self.ip}?fields=status,message,continent,country,regionName,city,isp,org,asname,query")
            result = response.json()
            if result.get("status") == "success":
                self.data = {
                    "IP": result.get("query"),
                    "Continent": result.get("continent"),
                    "Country": result.get("country"),
                    "Region": result.get("regionName"),
                    "City": result.get("city"),
                    "ISP": result.get("isp"),
                    "Organization": result.get("org"),
                    "AS Name": result.get("asname")
                }
            else:
                self.data = {"Error": result.get("message", "Unknown failure!")}
        except Exception as e:
            self.data = {"Error": str(e)}
        return self.data