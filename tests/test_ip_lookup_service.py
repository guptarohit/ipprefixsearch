import pytest
from src.services.ip_lookup_service import IPLookupService
from src.infrastructure.prefix_store import PrefixStore
from src.domain.models import IPPrefix


def setup_store_with_data():
    store = PrefixStore()
    store.add_prefix(
        IPPrefix(subnet="192.168.1.0/24", provider="ProviderA", tags=["Tag1"])
    )
    store.add_prefix(
        IPPrefix(subnet="2001:0db8::/32", provider="ProviderB", tags=["Tag2"])
    )
    return store


def test_lookup_single_ip():
    store = setup_store_with_data()
    service = IPLookupService(store)

    response = service.lookup_single_ip("192.168.1.10")
    assert len(response.result) == 1
    assert response.result[0].provider == "ProviderA"


def test_lookup_multiple_ips():
    store = setup_store_with_data()
    service = IPLookupService(store)

    response = service.lookup_multiple_ips(["192.168.1.10", "2001:0db8::1"])
    assert len(response) == 2
    assert response[0].result[0].provider == "ProviderA"
    assert response[1].result[0].provider == "ProviderB"


def test_lookup_no_match():
    store = setup_store_with_data()
    service = IPLookupService(store)

    response = service.lookup_single_ip("10.0.0.1")
    assert len(response.result) == 0


def test_invalid_ip():
    store = setup_store_with_data()
    service = IPLookupService(store)

    with pytest.raises(ValueError):
        service.lookup_single_ip("invalid_ip")
