from typing import List
from src.domain.models import IPPrefix
from src.infrastructure.ip_utils import parse_ip, parse_network
import json
from pathlib import Path
import ipaddress


class PrefixStore:
    def __init__(self):
        # Store parsed network objects with their metadata
        self.prefixes: List[tuple[ipaddress.ip_network, IPPrefix]] = []

    def add_prefix(self, prefix: IPPrefix):
        try:
            network = parse_network(prefix.subnet)
            self.prefixes.append((network, prefix))
        except ValueError:
            # Skip invalid prefixes
            pass

    def lookup_ip(self, ip: str) -> List[IPPrefix]:
        try:
            ip_obj = parse_ip(ip)
            return [
                prefix_data
                for network, prefix_data in self.prefixes
                if ip_obj in network
            ]
        except ValueError as e:
            raise ValueError(f"Invalid IP address: {ip}") from e

    @classmethod
    def from_json(cls, json_path: Path) -> "PrefixStore":
        store = cls()
        with open(json_path) as f:
            providers_data = json.load(f)

            for provider, provider_data in providers_data.items():
                for entry in provider_data:
                    tags = entry.get("tags", [])
                    for subnet in entry.get("prefixes", []):
                        prefix = IPPrefix(subnet=subnet, provider=provider, tags=tags)
                        store.add_prefix(prefix)
        return store
