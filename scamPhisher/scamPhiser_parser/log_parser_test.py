import unittest

from log_parser import *
from scamPhisher.logging.log_indexing import *
from unittest.mock import patch

class LogParserTesting(unittest.TestCase):
    """Main class for unit testing"""

    def setUp(self):
        self.logger = Logging(log_dir="logs/test")
        self.parser = LogParser()

    @patch(LogParser.parse_headers)
    def test_parse_header(self, mock_header):
        self.mock_header = {
            "From": r"^From: (.+)$",
            "Reply-To": r"^Reply-To: (.+)$",
            "Subject": r"^Subject: (.+)$",
            "Return-Path": r"^Return-Path: (.+)$",
            "X-Originating-Ip": r"^X-Originating-Ip: \[(.+)\]",
            "SPF": r"^Received-SPF: (.+)$",
            "DKIM": r"^DKIM-Signature: (.+)$",
            "Authentication-Results": r"^Authentication-Results: (.+)$"
            }
        
        result = self.parser.extract_all(self.mock_header)
        
        mock_header.assert_called_once_with(result)
        self.assertTrue()