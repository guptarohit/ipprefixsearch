import pytest
from src.services.ip_lookup_service import IPLookupService
from src.infrastructure.linear_prefix_store import LinearPrefixStore
from src.infrastructure.radix_prefix_store import RadixTreePrefixStore
from src.domain.models import IPPrefix


@pytest.fixture(params=[LinearPrefixStore, RadixTreePrefixStore])
def setup_store_with_data(request):
    store = request.param()
    store.add_prefix(
        IPPrefix(subnet="192.168.1.0/24", provider="ProviderA", tags=["Tag1"])
    )
    store.add_prefix(
        IPPrefix(subnet="2001:0db8::/32", provider="ProviderB", tags=["Tag2"])
    )
    return store


def test_lookup_single_ip(setup_store_with_data):
    service = IPLookupService(setup_store_with_data)

    response = service.lookup_single_ip("192.168.1.10")

    assert len(response.result) == 1
    assert response.result[0].provider == "ProviderA"
    assert response.result[0].tags == ["Tag1"]


def test_lookup_multiple_ips(setup_store_with_data):
    service = IPLookupService(setup_store_with_data)

    response = service.lookup_multiple_ips(["192.168.1.10", "2001:0db8::1"])
    assert len(response) == 2
    assert response[0].result[0].provider == "ProviderA"
    assert response[1].result[0].provider == "ProviderB"


def test_lookup_no_match(setup_store_with_data):
    service = IPLookupService(setup_store_with_data)

    response = service.lookup_single_ip("10.0.0.1")
    assert len(response.result) == 0


def test_lookup_invalid_ip(setup_store_with_data):
    service = IPLookupService(setup_store_with_data)

    with pytest.raises(ValueError):
        service.lookup_single_ip("invalid_ip")


def test_lookup_multiple_with_invalid(setup_store_with_data):
    service = IPLookupService(setup_store_with_data)

    with pytest.raises(ValueError):
        service.lookup_multiple_ips(["192.168.1.1", "invalid_ip"])


def test_empty_ip_list(setup_store_with_data):
    service = IPLookupService(setup_store_with_data)

    response = service.lookup_multiple_ips([])
    assert len(response) == 0
