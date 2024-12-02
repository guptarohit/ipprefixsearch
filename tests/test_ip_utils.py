import pytest
import ipaddress
from src.infrastructure.ip_utils import parse_ip, parse_network, is_ip_in_subnet


class TestIPUtils:
    # IPv4 Test Cases
    def test_parse_valid_ipv4(self):
        ip = parse_ip("192.168.1.1")
        assert isinstance(ip, ipaddress.IPv4Address)
        assert str(ip) == "192.168.1.1"

    def test_parse_valid_ipv4_network(self):
        network = parse_network("192.168.1.0/24")
        assert isinstance(network, ipaddress.IPv4Network)
        assert str(network) == "192.168.1.0/24"

    def test_ipv4_in_subnet(self):
        ip = parse_ip("192.168.1.100")
        network = parse_network("192.168.1.0/24")
        assert is_ip_in_subnet(ip, network) is True

    def test_ipv4_not_in_subnet(self):
        ip = parse_ip("192.168.2.1")
        network = parse_network("192.168.1.0/24")
        assert is_ip_in_subnet(ip, network) is False

    # IPv6 Test Cases
    def test_parse_valid_ipv6(self):
        ip = parse_ip("2001:db8::1")
        assert isinstance(ip, ipaddress.IPv6Address)
        assert str(ip) == "2001:db8::1"

    def test_parse_valid_ipv6_network(self):
        network = parse_network("2001:db8::/32")
        assert isinstance(network, ipaddress.IPv6Network)
        assert str(network) == "2001:db8::/32"

    def test_ipv6_in_subnet(self):
        ip = parse_ip("2001:db8::1")
        network = parse_network("2001:db8::/32")
        assert is_ip_in_subnet(ip, network) is True

    def test_ipv6_not_in_subnet(self):
        ip = parse_ip("2001:db9::1")
        network = parse_network("2001:db8::/32")
        assert is_ip_in_subnet(ip, network) is False

    # Error Cases
    def test_invalid_ip(self):
        with pytest.raises(ValueError, match="Invalid IP address:.*"):
            parse_ip("invalid.ip.address")

    def test_invalid_network(self):
        with pytest.raises(ValueError, match="Invalid CIDR format:.*"):
            parse_network("invalid/network")

    def test_malformed_ipv4(self):
        with pytest.raises(ValueError):
            parse_ip("256.256.256.256")

    def test_malformed_ipv6(self):
        with pytest.raises(ValueError):
            parse_ip("2001:zzzz::1")

    def test_malformed_network_prefix(self):
        with pytest.raises(ValueError):
            parse_network("192.168.1.0/33")  # Invalid prefix length
