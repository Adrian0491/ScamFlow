import unittest

from log_parser import *
from scamPhisher.logging.log_indexing import *
from unittest.mock import patch

class LogParserTesting(unittest.TestCase):
    """Main class for unit testing"""

    def setUp(self):
        self.test_mail = (
            "From: attacker@malicious.com\n"
            "Reply-To: scam@fraud.net\n"
            "Subject: Urgent Job Offer\n"
            "Return-Path: <bounce@spoofed.net>\n"
            "X-Originating-Ip: [10.0.0.1]\n"
            "Received-SPF: fail\n"
            "DKIM-Signature: some_dkim_value\n"
            "Authentication-Result: fail\n"
            "\n"
            "Links: https://scamlink.net/verify"
        )
        self.parser = LogParser(raw_email=self.test_mail)

    def test_header_extraction(self):
        result = self.parser.extract_all()

        self.assertEqual(result["From"], "attacker@malicious.com")
        self.assertEqual(result["Reply-To"], "scam@fraud.net")
        self.assertEqual(result["Subject"], "Urgent Job Offer")
        self.assertEqual(result["Return-Path"], "<bounce@spoofed.net>")
        self.assertEqual(result["X-Originating-Ip"], "10.0.0.1")
        self.assertEqual(result["SPF"], "fail")
        self.assertEqual(result["DKIM"], "some_dkim_value")

    def test_link_extraction(self):
        result = self.parser.extract_all()

        self.assertIn("https://scamlink.net/verify", result["Links"])

    def test_json_export(self):
        self.parser.extract_all()
        self.parser.save_to_json("test_output.json")

        with open("test_output.json", "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("attacker@malicious.com", content)
            self.assertIn("https://scamlink.net/verify", content)

if __name__ == '__main__':
    unittest.main()