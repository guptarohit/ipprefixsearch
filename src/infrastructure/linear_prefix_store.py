from typing import List
from src.domain.models import IPPrefix
import ipaddress

from src.infrastructure.ip_utils import parse_ip, parse_network

from src.infrastructure.prefix_store import AbstractPrefixStore


class LinearPrefixStore(AbstractPrefixStore):
    def __init__(self):
        self.prefixes: List[tuple[ipaddress.ip_network, IPPrefix]] = []

    def add_prefix(self, prefix: IPPrefix) -> None:
        try:
            network = parse_network(prefix.subnet)
            self.prefixes.append((network, prefix))
        except ValueError:
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
