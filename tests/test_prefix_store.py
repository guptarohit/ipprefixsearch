import pytest

from src.infrastructure.linear_prefix_store import LinearPrefixStore
from src.infrastructure.radix_prefix_store import RadixTreePrefixStore
from src.domain.models import IPPrefix
from src.infrastructure.prefix_store_factory import PrefixStoreFactory
from pathlib import Path


@pytest.fixture(params=[LinearPrefixStore, RadixTreePrefixStore])
def prefix_store(request):
    """Fixture that provides both store implementations for testing."""
    return request.param()


def test_add_and_lookup_ipv4(prefix_store):
    prefix = IPPrefix(subnet="192.168.1.0/24", provider="ProviderA", tags=["Tag1"])
    prefix_store.add_prefix(prefix)

    result = prefix_store.lookup_ip("192.168.1.10")
    assert len(result) == 1
    assert result[0].provider == "ProviderA"
    assert result[0].tags == ["Tag1"]


def test_add_and_lookup_ipv6(prefix_store):
    prefix = IPPrefix(subnet="2001:0db8::/32", provider="ProviderB", tags=["Tag2"])
    prefix_store.add_prefix(prefix)

    result = prefix_store.lookup_ip("2001:0db8::1")
    assert len(result) == 1
    assert result[0].provider == "ProviderB"
    assert result[0].tags == ["Tag2"]


def test_lookup_no_match(prefix_store):
    prefix = IPPrefix(subnet="10.0.0.0/8", provider="ProviderC", tags=["Tag3"])
    prefix_store.add_prefix(prefix)

    result = prefix_store.lookup_ip("192.168.1.10")
    assert len(result) == 0


def test_invalid_ip(prefix_store):
    with pytest.raises(ValueError, match="Invalid IP address:.*"):
        prefix_store.lookup_ip("invalid_ip")


def test_invalid_subnet(prefix_store):
    prefix = IPPrefix(subnet="invalid_subnet", provider="ProviderD", tags=["Tag4"])
    prefix_store.add_prefix(prefix)  # Should silently ignore invalid subnet


def test_multiple_matches(prefix_store):
    # Add overlapping prefixes
    prefix1 = IPPrefix(subnet="10.0.0.0/8", provider="ProviderA", tags=["TagA"])
    prefix2 = IPPrefix(subnet="10.0.0.0/16", provider="ProviderB", tags=["TagB"])
    prefix_store.add_prefix(prefix1)
    prefix_store.add_prefix(prefix2)

    result = prefix_store.lookup_ip("10.0.0.5")
    assert len(result) == 2
    providers = {r.provider for r in result}
    assert providers == {"ProviderA", "ProviderB"}


def test_factory_creation():
    # Create a temporary JSON file for testing
    test_data = {
        "TestProvider": [{"prefixes": ["192.168.0.0/24"], "tags": ["TestTag"]}]
    }
    tmp_path = Path("test_prefixes.json")

    try:
        import json

        with open(tmp_path, "w") as f:
            json.dump(test_data, f)

        # Test both implementations using the factory
        for store_class in [LinearPrefixStore, RadixTreePrefixStore]:
            store = PrefixStoreFactory.create_from_json(store_class, tmp_path)
            result = store.lookup_ip("192.168.0.1")
            assert len(result) == 1
            assert result[0].provider == "TestProvider"
            assert result[0].tags == ["TestTag"]

    finally:
        # Cleanup
        if tmp_path.exists():
            tmp_path.unlink()


def test_empty_store(prefix_store):
    result = prefix_store.lookup_ip("192.168.1.1")
    assert len(result) == 0


def test_add_multiple_prefixes(prefix_store):
    prefixes = [
        IPPrefix(subnet="192.168.1.0/24", provider="Provider1", tags=["Tag1"]),
        IPPrefix(subnet="10.0.0.0/8", provider="Provider2", tags=["Tag2"]),
        IPPrefix(subnet="172.16.0.0/12", provider="Provider3", tags=["Tag3"]),
    ]

    for prefix in prefixes:
        prefix_store.add_prefix(prefix)

    # Test each prefix
    assert len(prefix_store.lookup_ip("192.168.1.1")) == 1
    assert len(prefix_store.lookup_ip("10.0.0.1")) == 1
    assert len(prefix_store.lookup_ip("172.16.0.1")) == 1
