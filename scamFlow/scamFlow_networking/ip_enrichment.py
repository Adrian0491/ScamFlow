import requests
import json
import os
import glob
from typing import Dict, Optional

# Optional: Define the folder containing parsed JSON files
JSON_DIR = "scamFlow/JSON_Output"

class IPEnricher:
    """
    A utility class to enrich IP address metadata using the ip-api.com service.

    It retrieves geolocation, ISP, organization, and ASN information for a given IP
    which can assist in identifying infrastructure used in scam or phishing activity.
    """
    def __init__(self, ip_address: str):
        self.ip = ip_address
        self.data: Dict[str, Optional[str]] = {}

    def enrich_ip(self) -> Dict[str, Optional[str]]:
        try:
            response = requests.get(
                f"http://ip-api.com/json/{self.ip}?fields=status,message,continent,country,regionName,city,isp,org,asname,query"
            )
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
                self.data = {"Error": result.get("message", "Unknown failure")}
        except Exception as e:
            self.data = {"Error": str(e)}
        return self.data

if __name__ == "__main__":
    json_files = glob.glob(os.path.join(JSON_DIR, "*.json"))

    for json_file in json_files:
        print(f"\n🔍 Processing: {os.path.basename(json_file)}")
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            ip = data.get("X-Originating-Ip")
            if ip:
                enricher = IPEnricher(ip)
                enriched = enricher.enrich_ip()
                print(json.dumps(enriched, indent=4))
            else:
                print("[INFO] No X-Originating-Ip found.")
        except Exception as e:
            print(f"[ERROR] Failed to process {json_file}: {e}")
