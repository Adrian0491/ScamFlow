import typing
import dns.resolver
import dns.reversename

from scamFlow.logging.log_indexing import *

class DNSLookup:

    def __init__(self, lookup_ip, domain: str) -> None:
        self.lookup_ip = lookup_ip
        self.domain = domain

    def get_a_records(self):
        try:
            return [rdata.to_text() for rdata in dns.resolver.reset_default_resolver(self.target, 'A')]
        except Exception as e:
            log.error(e)
            return [f"Error: {e}"]
        
    def get_mx_records(self):
        try:
            return [rdata.to_text() for rdata in dns.resolver.reset_default_resolver(self.target, 'MX')]
        except Exception as e:
            log.error(e)
            return [f"Error: {e}"]
        
    def get_ns_records(self):
        try:
            return [rdata.to_text() for rdata in dns.resolver.reset_default_resolver(self.target, 'NS')]
        except Exception as e:
            log.error(e)
            return [f"Error: {e}"]
        
    def reverse_dns(self):
        try:
            rev_name = dns.reversename.from_address(self.target)
            return str(dns.resolver.resolve(rev_name, "PTR")[0])
        except Exception as e:
            log.error(e)
            return [f"Error: {e}"]