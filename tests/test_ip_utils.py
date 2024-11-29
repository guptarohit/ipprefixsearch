import pytest
from src.infrastructure.ip_utils import ip_to_int, parse_cidr, is_ip_in_subnet


def test_ip_to_int():
    assert ip_to_int("192.168.1.1") == 3232235777
    assert ip_to_int("0.0.0.0") == 0
    assert ip_to_int("255.255.255.255") == 4294967295


def test_ip_to_int_invalid():
    with pytest.raises(ValueError):
        ip_to_int("192.168.1")
    with pytest.raises(ValueError):
        ip_to_int("192.168.1.256")
    with pytest.raises(ValueError):
        ip_to_int("192.168.1.-1")


def test_parse_cidr():
    network, mask, prefix_len = parse_cidr("192.168.1.0/24")
    assert prefix_len == 24
    assert network == 3232235776  # 192.168.1.0
    assert mask == 4294967040  # 255.255.255.0


def test_is_ip_in_subnet():
    # Test for 192.168.1.0/24
    network, mask, _ = parse_cidr("192.168.1.0/24")

    # IP in subnet
    ip = ip_to_int("192.168.1.100")
    assert is_ip_in_subnet(ip, network, mask)

    # IP not in subnet
    ip = ip_to_int("192.168.2.100")
    assert not is_ip_in_subnet(ip, network, mask)
