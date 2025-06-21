import unittest
import types

from ip_enrichment import *
from unittest.mock import *
from typing import Dicts

JSON_DIR = "scamFlow/JSON_Output"


class IPEnrichmentTesting(unittest.TestCase):
    
    @patch('scamFlow.scamFlow_networking.ip_enrichment.requests.get')
    def test_enrich_ip(self, mock_get):
         mock_response = Mock()
         mock_response.json.return_value = {
              "status": "success",
              "query": "8.8.8.8",
              "continent": "North America",
              "country": "United States",
              "regionName": "Texas",
              "city": "San Antonio",
              "isp": "DummyNet LLC",
              "org": "CloudSharex",
              "asname": "AS151983 DummyNet LLC"
         }
         mock_get.return_value = mock_response
         enricher = IPEnricher("8.8.8.8")
         result = enricher.enrich_ip()

         self.assertEqual(result["IP"], "8.8.8.8")
         self.assertEqual(result["City"], "San Antonio")

class TestAbuseChecker(unittest.TestCase):
     
     @patch('scamFlow.scamFlow_networking.ip_enrichment.requests.get')
     def test_abuse_checker_score(self, mock_get):
          """"""