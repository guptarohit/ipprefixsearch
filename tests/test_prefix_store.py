import pytest
from src.infrastructure.prefix_store import PrefixStore
from src.domain.models import IPPrefix


def test_add_and_lookup_ipv4():
    store = PrefixStore()
    prefix = IPPrefix(subnet="192.168.1.0/24", provider="ProviderA", tags=["Tag1"])
    store.add_prefix(prefix)

    result = store.lookup_ip("192.168.1.10")
    assert len(result) == 1
    assert result[0].provider == "ProviderA"
    assert result[0].tags == ["Tag1"]


def test_add_and_lookup_ipv6():
    store = PrefixStore()
    prefix = IPPrefix(subnet="2001:0db8::/32", provider="ProviderB", tags=["Tag2"])
    store.add_prefix(prefix)

    result = store.lookup_ip("2001:0db8::1")
    assert len(result) == 1
    assert result[0].provider == "ProviderB"
    assert result[0].tags == ["Tag2"]


def test_lookup_no_match():
    store = PrefixStore()
    prefix = IPPrefix(subnet="10.0.0.0/8", provider="ProviderC", tags=["Tag3"])
    store.add_prefix(prefix)

    result = store.lookup_ip("192.168.1.10")
    assert len(result) == 0


def test_invalid_ip():
    store = PrefixStore()
    with pytest.raises(ValueError):
        store.lookup_ip("invalid_ip")


def test_invalid_subnet():
    store = PrefixStore()
    prefix = IPPrefix(subnet="invalid_subnet", provider="ProviderD", tags=["Tag4"])
    store.add_prefix(prefix)

    # Ensure no prefixes are added for invalid subnets
    assert len(store.prefixes) == 0
