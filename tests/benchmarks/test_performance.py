import pytest
import time
from src.infrastructure.linear_prefix_store import LinearPrefixStore
from src.infrastructure.radix_prefix_store import RadixTreePrefixStore
from src.services.ip_lookup_service import IPLookupService
from src.infrastructure.prefix_store_factory import PrefixStoreFactory
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent.parent
json_path = project_root / "prefixes.json"


@pytest.fixture(params=[LinearPrefixStore, RadixTreePrefixStore])
def ip_service(request):
    store = PrefixStoreFactory.create_from_json(request.param, json_path)
    return IPLookupService(store)


def test_single_ip_lookup_performance(ip_service):
    ip = "184.51.33.230"

    start_time = time.perf_counter()
    ip_service.lookup_single_ip(ip)
    elapsed_time = (time.perf_counter() - start_time) * 1000  # Convert to milliseconds

    assert (
        elapsed_time < 50
    ), f"Single IP lookup took {elapsed_time}ms, should be under 50ms"


def test_batch_ip_lookup_performance(ip_service):
    ips = [
        "184.51.33.230",
        "184.51.33.231",
        "184.51.33.232",
        "184.51.33.233",
        "184.51.33.234",
        "184.51.33.235",
        "184.51.33.236",
        "184.51.33.237",
        "184.51.33.238",
        "184.51.33.239",
    ]

    start_time = time.perf_counter()
    ip_service.lookup_multiple_ips(ips)
    elapsed_time = (time.perf_counter() - start_time) * 1000  # Convert to milliseconds

    assert (
        elapsed_time < 300
    ), f"Batch IP lookup took {elapsed_time}ms, should be under 300ms"


def test_performance_comparison():
    """Compare performance between LinearPrefixStore and RadixTreePrefixStore"""
    ips = [f"184.51.33.{i}" for i in range(10)]
    results = {}

    for store_class in [LinearPrefixStore, RadixTreePrefixStore]:
        store = PrefixStoreFactory.create_from_json(store_class, json_path)
        service = IPLookupService(store)

        start_time = time.perf_counter()
        service.lookup_multiple_ips(ips)
        elapsed_time = (time.perf_counter() - start_time) * 1000
        results[store_class.__name__] = elapsed_time

    print("\nPerformance comparison for 10 IPs:")
    for name, time_ms in results.items():
        print(f"{name}: {time_ms:.2f}ms")

    # RadixTree should be faster than Linear for larger datasets
    assert (
        results["RadixTreePrefixStore"] < results["LinearPrefixStore"]
    ), f"RadixTree implementation should be at least as fast as Linear implementation, {results}"
