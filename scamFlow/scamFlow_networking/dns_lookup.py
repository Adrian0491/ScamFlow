import dns.resolver
import dns.reversename
from scamFlow.logging.log_indexing import Logging

class DNSLookup:
    
    """
    DNSLookup provides DNS queries (A, MX, NS) and reverse DNS lookups,
    with centralized logging for failures.
    """

    def __init__(self, lookup_ip: str = None, domain: str = None):
        self.lookup_ip = lookup_ip
        self.domain = domain
        self.logger = Logging()

    def get_a_records(self):
        try:
            return [rdata.to_text() for rdata in dns.resolver.resolve(self.domain, 'A')]
        except Exception as e:
            self.logger.error(f"A record lookup failed for {self.domain}: {e}")
            return [f"Error: {e}"]

    def get_mx_records(self):
        try:
            return [rdata.exchange.to_text() for rdata in dns.resolver.resolve(self.domain, 'MX')]
        except Exception as e:
            self.logger.error(f"MX record lookup failed for {self.domain}: {e}")
            return [f"Error: {e}"]

    def get_ns_records(self):
        try:
            return [rdata.to_text() for rdata in dns.resolver.resolve(self.domain, 'NS')]
        except Exception as e:
            self.logger.error(f"NS record lookup failed for {self.domain}: {e}")
            return [f"Error: {e}"]

    def reverse_dns(self):
        try:
            rev_name = dns.reversename.from_address(self.lookup_ip)
            return str(dns.resolver.resolve(rev_name, "PTR")[0])
        except Exception as e:
            self.logger.error(f"Reverse DNS lookup failed for {self.lookup_ip}: {e}")
            return f"Error: {e}"

    def to_dict(self):
        result = {}
        if self.domain:
            result["A Records"] = self.get_a_records()
            result["MX Records"] = self.get_mx_records()
            result["NS Records"] = self.get_ns_records()
        if self.lookup_ip:
            result["Reverse DNS"] = self.reverse_dns()
        return result
