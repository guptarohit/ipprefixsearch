import ipaddress
from typing import Union

IPAddress = Union[ipaddress.IPv4Address, ipaddress.IPv6Address]
IPNetwork = Union[ipaddress.IPv4Network, ipaddress.IPv6Network]


def parse_ip(ip: str) -> IPAddress:
    """Convert IP address string to IPv4Address or IPv6Address object."""
    try:
        return ipaddress.ip_address(ip)
    except ValueError as e:
        raise ValueError(f"Invalid IP address: {ip}") from e


def parse_network(subnet: str) -> IPNetwork:
    """Parse CIDR notation into an IP network object."""
    try:
        return ipaddress.ip_network(subnet)
    except ValueError as e:
        raise ValueError(f"Invalid CIDR format: {subnet}") from e


def is_ip_in_subnet(ip: IPAddress, network: IPNetwork) -> bool:
    """Check if IP is in subnet."""
    return ip in network
