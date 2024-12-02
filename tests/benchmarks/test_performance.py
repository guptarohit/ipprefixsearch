import pytest
import time
from src.infrastructure.prefix_store import PrefixStore
from src.services.ip_lookup_service import IPLookupService
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.parent.parent
json_path = project_root / "prefixes.json"


@pytest.fixture
def ip_service():
    prefix_store = PrefixStore.from_json(json_path)
    return IPLookupService(prefix_store)


def test_single_ip_lookup_performance(ip_service):
    ip = "184.51.33.230"

    start_time = time.time()
    ip_service.lookup_single_ip(ip)
    elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds

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

    start_time = time.time()
    ip_service.lookup_multiple_ips(ips)
    elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds

    assert (
        elapsed_time < 300
    ), f"Batch IP lookup took {elapsed_time}ms, should be under 300ms"
