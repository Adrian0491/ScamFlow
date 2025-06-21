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
    
class AbuseChecker:
    """
        Checks if the IP has been reported for malicious activity using the Abuse IPDB API.
        Returns abuse confidence score, number of reports and the country.
    """
    API_KEY = "f0c1c15a593602824a2e30c770a696f2fe03e7be68e7076a8fde1d1e87958f08e0143b69a53d3a34"
    API_URL = "https://api.abuseipdb.com/api/v2/check"

    def __init__(self, ip: str):
        self.ip = ip
        self.headers = {
            "Key": self.API_KEY,
            "Accept": "application/json"
        }
        self.data = Dict[str, Optional[str]] = {}

    def abuse_checker(self) -> Dict[str, Optional[str]]:
        try:
            response = requests.get(
                self.API_URL,
                headers = self.headers,
                params={"ipAddress": self.ip, "maxAgeInDays": 90}
            )
            result = response.json()["data"]
            self.data = {
                "Abuse Score": str(result.get("abuseConfidenceScore")),
                "Reported Times": str(result.get("totalReports")),
                "Last Reported": result.get("lastReportedAt"),
                "Abuse Country": result.get("countryCode"),
            }            
        except Exception as e:
            self.data = {f"Error": str(e)}
        return self.data
    
class GeoLocator:
    """
        Uses ipinfo.io to fetch geolocation, hosting type and privacy info.
        Includes detection of VPN, hosting provider or Tor exit node.
    """

    TOKEN = "93a9efc5b15921"
    API_URL = "https://ipinfo.io"

    def __init__(self, ip_address: str):
        self.ip = ip_address
        self.data: Dict[str, Optional[str]] = {}

    def lookup_geo(self) -> Dict[str, Optional[str]]:
        try:
            response = requests.get(f"{self.API_URL}/{self.ip}?token={self.TOKEN}")
            result = response.json()
            self.data = {
                "IP": result.get("ip"),
                "City": result.get("city"),
                "Region": result.get("region"),
                "Country": result.get("country"),
                "Org": result.get("org"),
                "Hostname": result.get("hostname"),
                "Anycast": str(result.get("anycast")),
                "Bogon": str(result.get("bogon")),
                "Privacy": str(response.get("privacy")),
            }
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
                
                results = {}

                enricher = IPEnricher(ip)
                results["IPEnricher"] = enricher.enrich_ip()

                abuse = AbuseChecker(ip)
                results["AbuseChecker"] = abuse.abuse_checker()

                locator = GeoLocator(ip)
                results["GeoLocator"] = locator.lookup_geo()
              
                print(json.dump(results, indent=4))

                output_file = os.path.splitext(json_file)[0] + "_enriched.json"
                with open(output_file, "w", encoding="utf-8") as outf:
                    json.dump(results, outf, indent=4)
            else:
                print("[INFO] No X-Originating-Ip found.")
        except Exception as e:
            print(f"[ERROR] Failed to process {json_file}: {e}")
