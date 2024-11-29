from typing import Tuple


def ip_to_int(ip: str) -> int:
    """Convert IP address string to 32-bit integer."""
    parts = ip.split(".")
    if len(parts) != 4:
        raise ValueError(f"Invalid IP address format: {ip}")

    result = 0
    for part in parts:
        octet = int(part)
        if not 0 <= octet <= 255:
            raise ValueError(f"Invalid IP address octet: {octet}")
        result = (result << 8) | octet
    return result


def parse_cidr(subnet: str) -> Tuple[int, int, int]:
    """
    Parse CIDR notation (e.g., '192.168.1.0/24') into network address and mask.
    Returns (network_address, mask, prefix_length)
    """
    try:
        ip, prefix_len = subnet.split("/")
        prefix_len = int(prefix_len)
        if not 0 <= prefix_len <= 32:
            raise ValueError(f"Invalid prefix length: {prefix_len}")

        ip_int = ip_to_int(ip)
        mask = ((1 << 32) - 1) << (32 - prefix_len)
        network_address = ip_int & mask

        return network_address, mask, prefix_len
    except ValueError as e:
        raise ValueError(f"Invalid CIDR format: {subnet}") from e


def is_ip_in_subnet(ip: int, network: int, mask: int) -> bool:
    """Check if IP is in subnet using bitwise operations."""
    return (ip & mask) == network
