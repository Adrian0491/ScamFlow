import unittest
from unittest.mock import patch, Mock
from scamFlow.scamFlow_networking.dns_lookup import DNSLookup

class TestDNSLookup(unittest.TestCase):

    @patch("dns.resolver.resolve")
    def test_get_a_records(self, mock_resolve):
        mock_resolve.return_value = [Mock(to_text=lambda: "93.184.216.34")]
        lookup = DNSLookup(domain="example.com")
        result = lookup.get_a_records()
        self.assertIn("93.184.216.34", result)

    @patch("dns.resolver.resolve")
    def test_get_mx_records(self, mock_resolve):
        mock_resolve.return_value = [Mock(exchange=Mock(to_text=lambda: "mail.example.com"))]
        lookup = DNSLookup(domain="example.com")
        result = lookup.get_mx_records()
        self.assertIn("mail.example.com", result)

    @patch("dns.resolver.resolve")
    def test_get_ns_records(self, mock_resolve):
        mock_resolve.return_value = [Mock(to_text=lambda: "ns1.example.com")]
        lookup = DNSLookup(domain="example.com")
        result = lookup.get_ns_records()
        self.assertIn("ns1.example.com", result)

    @patch("dns.reversename.from_address")
    @patch("dns.resolver.resolve")
    def test_reverse_dns(self, mock_resolve, mock_reverse):
        mock_reverse.return_value = "34.216.184.93.in-addr.arpa"
        mock_resolve.return_value = ["example.com."]
        lookup = DNSLookup(lookup_ip="93.184.216.34")
        result = lookup.reverse_dns()
        self.assertEqual(result, "example.com.")

if __name__ == "__main__":
    unittest.main()
