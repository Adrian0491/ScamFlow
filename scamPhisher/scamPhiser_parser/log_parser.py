import re
import json
import sys
import os

from typing import Optional, Dict, List, Union
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from scamPhisher.logging.log_indexing import Logging

class LogParser:
    def __init__(self, raw_email: str):
        self.raw_email = raw_email
        self.parsed_data: Dict[str, Union[Optional[str], List[str]]] = {}
        self.logger = Logging()

    def parse_headers(self) -> None:
        """Extract common headers from the raw email."""
        headers = {
            "From": r"^From: (.+)$",
            "Reply-To": r"^Reply-To: (.+)$",
            "Subject": r"^Subject: (.+)$",
            "Return-Path": r"^Return-Path: (.+)$",
            "X-Originating-Ip": r"^X-Originating-Ip: \[(.+)\]",
            "SPF": r"^Received-SPF: (.+)$",
            "DKIM": r"^DKIM-Signature: (.+)$",
            "Authentication-Results": r"^Authentication-Results: (.+)$",
        }
        for key, pattern in headers.items():
            match = re.search(pattern, self.raw_email, re.MULTILINE)
            self.parsed_data[key] = match.group(1).strip() if match else None

        # Log essential extracted header data
        log_msg = (
            f"From: {self.parsed_data.get('From')} | "
            f"X-Originating-IP: {self.parsed_data.get('X-Originating-Ip')} | "
            f"DateTime: {datetime.now().strftime('%m-%d-%y %H:%M')}"
        )
        self.logger.info(log_msg)

    def extract_links(self) -> None:
        """Extract all HTTP/HTTPS links from the email."""
        links = re.findall(r"https?://[\w\.-]+(?:/[\w\./\-\?=&%]*)?", self.raw_email)
        self.parsed_data["Links"] = links if links else []

    def extract_all(self) -> Dict[str, Union[Optional[str], List[str]]]:
        """Run all parsing steps."""
        self.parse_headers()
        self.extract_links()
        return self.parsed_data

    def save_to_json(self, output_path: str = "parsed_email.json") -> None:
        """Save the parsed data to a JSON file."""
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.parsed_data, f, indent=4, ensure_ascii=False)