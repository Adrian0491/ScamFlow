import re
import json
import sys
import os
import glob

from typing import Optional, Dict, List, Union
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from scamPhisher.logging.log_indexing import Logging

# Constants for paths
RAW_MESSAGE_PATH = "scamPhisher/raw_messages_models"
JSON_OUTPUT_PATH = "scamPhisher/JSON_Output"
LOGS_DIR = "scamPhisher/logs"
LOG_FILE_NAME = "scamFlow.log"

class LogParser:
    def __init__(self, raw_email: str):
        self.raw_email = raw_email
        self.parsed_data: Dict[str, Union[Optional[str], List[str]]] = {}
        self.logger = Logging(log_dir = LOGS_DIR, log_file=LOG_FILE_NAME) 

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

    def parse_all_files(self, input_dir: str = RAW_MESSAGE_PATH, output_dir: str = JSON_OUTPUT_PATH) -> None:
        """
        Parses all files contained by the raw_messages_module Folder.
        Output is saved in a JSON file.
        """
        files = glob.glob(os.path.join(input_dir, "*.log")) + glob.glob(os.path.join(input_dir, "*.eml"))

        for file_path in files:
            with open(file_path, "r", encoding="utf-8") as f:
                self.raw_email = f.read()
                self.parsed_data = {}
                self.extract_all()

                base_name = os.path.splitext(os.path.basename(file_path))[0]
                output_path = os.path.join(output_dir, f"{base_name}_parsed.json")
                with open(output_path, "w", encoding="utf-8") as out_file:
                    json.dump(self.parsed_data, out_file, indent=4, ensure_ascii=False)
                self.logger.info(f"Parsed and saved: {output_path}")

if __name__ == "__main__":
    parser = LogParser("") # Empty string, as the content is replaced per file
    parser.parse_all_files()