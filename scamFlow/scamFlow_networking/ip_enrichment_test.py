import unittest
import os
import sys

from unittest.mock import patch, Mock
#from scamFlow.scamFlow_networking.ip_enrichment import *


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),"../../..")))
class TestIPEnricher(unittest.TestCase):
    @patch('scamFlow.scamFlow_networking.ip_enrichment.requests.get')
    def test_enrich_ip_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "status": "success",
            "query": "8.8.8.8",
            "continent": "North America",
            "country": "United States",
            "regionName": "California",
            "city": "Mountain View",
            "isp": "Google LLC",
            "org": "Google Public DNS",
            "asname": "AS15169 Google LLC"
        }
        mock_get.return_value = mock_response

        enricher = IPEnricher("8.8.8.8")
        result = enricher.enrich_ip()

        self.assertEqual(result["IP"], "8.8.8.8")
        self.assertEqual(result["City"], "Mountain View")


class TestAbuseChecker(unittest.TestCase):
    @patch('scamFlow.scamFlow_networking.ip_enrichment.requests.get')
    def test_abuse_checker_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "data": {
                "abuseConfidenceScore": 10,
                "totalReports": 5,
                "lastReportedAt": "2023-11-01T12:00:00Z",
                "countryCode": "US"
            }
        }
        mock_get.return_value = mock_response

        with patch.object(AbuseChecker, 'API_KEY', "dummy_api_key"):
            checker = AbuseChecker("8.8.8.8")
            result = checker.abuse_checker()

        self.assertEqual(result["Abuse Score"], "10")
        self.assertEqual(result["Abuse Country"], "US")


class TestGeoLocator(unittest.TestCase):
    @patch('scamFlow.scamFlow_networking.ip_enrichment.requests.get')
    def test_geo_locator_success(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {
            "ip": "8.8.8.8",
            "city": "Mountain View",
            "region": "California",
            "country": "US",
            "org": "Google LLC",
            "hostname": "dns.google",
            "anycast": True,
            "bogon": False,
            "privacy": {"vpn": False}
        }
        mock_get.return_value = mock_response

        with patch.object(GeoLocator, 'TOKEN', "dummy_token"):
            locator = GeoLocator("8.8.8.8")
            result = locator.lookup_geo()

        self.assertEqual(result["IP"], "8.8.8.8")
        self.assertEqual(result["City"], "Mountain View")


if __name__ == '__main__':
    unittest.main()
