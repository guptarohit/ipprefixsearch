from typing import List, Dict
from src.domain.models import IPPrefix
from src.infrastructure.ip_utils import ip_to_int, parse_cidr, is_ip_in_subnet
import json
from pathlib import Path


class PrefixStore:
    def __init__(self):
        # Store prefixes grouped by first octet for quick filtering
        self.prefix_map: Dict[int, List[tuple[int, int, IPPrefix]]] = {}

    def add_prefix(self, prefix: IPPrefix):
        network_addr, mask, prefix_len = parse_cidr(prefix.subnet)
        first_octet = network_addr >> 24

        if first_octet not in self.prefix_map:
            self.prefix_map[first_octet] = []

        # Store (network_address, mask, prefix_data) tuple
        self.prefix_map[first_octet].append((network_addr, mask, prefix))

    def lookup_ip(self, ip: str) -> List[IPPrefix]:
        try:
            ip_int = ip_to_int(ip)
            first_octet = ip_int >> 24

            results = []
            if first_octet not in self.prefix_map:
                return results

            # Check all prefixes in the matching first octet bucket
            for network_addr, mask, prefix in self.prefix_map[first_octet]:
                if is_ip_in_subnet(ip_int, network_addr, mask):
                    results.append(prefix)

            return results

        except ValueError as e:
            raise ValueError(f"Invalid IP address: {ip}") from e

    @classmethod
    def from_json(cls, json_path: Path) -> "PrefixStore":
        store = cls()
        with open(json_path) as f:
            providers_data = json.load(f)

            # Iterate through each provider
            for provider, provider_data in providers_data.items():
                for entry in provider_data:
                    # Get tags for this group of prefixes
                    tags = entry.get("tags", [])

                    # Process each prefix in the group
                    for subnet in entry["prefixes"]:
                        try:
                            prefix = IPPrefix(
                                subnet=subnet, provider=provider, tags=tags
                            )
                            store.add_prefix(prefix)
                        except Exception as _:
                            continue

        return store
