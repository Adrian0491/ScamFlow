import unittest

from unittest.mock import Mock, patch
from scamFlow.scamFlow_networking.dns_lookup import *

class dnsLookupTesting(unittest.TestCase):
    """Unit testing class for the DNS Lookup"""

    @patch("dns.resolver.resolve")
    def test_get_a_records(self, mock_resolve):
        
        mock_resolve.resolve_value = [Mock(to_text=lambda: "93.184.216.34")]
        lookup = DNSLookup(domain="example.com")
        dnsLookupResult = lookup.get_a_records()
        
        self.assertIn("93.184.216.34", dnsLookupResult)

    @patch("dns.resolver.resolve")
    def test_get_mx_records(self, mock_resolve):

        mock_resolve.reslove = [Mock(to_text=lambda: "mail.example.com")]