from typing import List, Dict
from src.domain.models import IPPrefix
from src.infrastructure.prefix_store import AbstractPrefixStore
from src.infrastructure.ip_utils import parse_ip, parse_network


class RadixNode:
    def __init__(self):
        self.children: Dict[str, "RadixNode"] = {}
        self.prefixes: List[IPPrefix] = []


class RadixTreePrefixStore(AbstractPrefixStore):
    def __init__(self):
        self.root = RadixNode()

    def add_prefix(self, prefix: IPPrefix) -> None:
        try:
            network = parse_network(prefix.subnet)
            addr_bits = format(
                int(network.network_address), f"0{network.max_prefixlen}b"
            )
            prefix_bits = addr_bits[: network.prefixlen]

            node = self.root
            for bit in prefix_bits:
                if bit not in node.children:
                    node.children[bit] = RadixNode()
                node = node.children[bit]

            node.prefixes.append(prefix)

        except ValueError:
            pass

    def lookup_ip(self, ip: str) -> List[IPPrefix]:
        try:
            ip_obj = parse_ip(ip)
            addr_bits = format(int(ip_obj), f"0{ip_obj.max_prefixlen}b")

            matches: List[IPPrefix] = []
            node = self.root

            for bit in addr_bits:
                matches.extend(node.prefixes)
                if bit not in node.children:
                    break
                node = node.children[bit]
            return matches

        except ValueError as e:
            raise ValueError(f"Invalid IP address: {ip}") from e
