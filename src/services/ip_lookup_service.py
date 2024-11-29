from typing import List
from src.domain.models import IPLookupResult, IPLookupResponse
from src.infrastructure.prefix_store import PrefixStore


class IPLookupService:
    def __init__(self, prefix_store: PrefixStore):
        self.prefix_store = prefix_store

    def lookup_single_ip(self, ip: str) -> IPLookupResponse:
        matches = self.prefix_store.lookup_ip(ip)
        results = [
            IPLookupResult(
                subnet=prefix.subnet, provider=prefix.provider, tags=prefix.tags
            )
            for prefix in matches
        ]
        return IPLookupResponse(result=results)

    def lookup_multiple_ips(self, ips: List[str]) -> List[IPLookupResponse]:
        return [self.lookup_single_ip(ip) for ip in ips]
