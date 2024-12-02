from fastapi import APIRouter, HTTPException, Query
from typing import List
from src.domain.models import IPLookupResponse
from src.services.ip_lookup_service import IPLookupService
from src.infrastructure.prefix_store import PrefixStore
from pathlib import Path

router = APIRouter(prefix="/ips")

# Get the project root directory
project_root = Path(__file__).parent.parent.parent
json_path = project_root / "prefixes.json"

prefix_store = PrefixStore.from_json(json_path)
ip_service = IPLookupService(prefix_store)


@router.get("/{ip}", response_model=IPLookupResponse)
def get_ip_info(ip: str) -> IPLookupResponse:
    """
    Get provider and tag information for a single IP address.
    """
    try:
        return ip_service.lookup_single_ip(ip)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=List[IPLookupResponse])
def get_ips_info(
    ips: List[str] = Query(..., description="List of IP addresses to lookup"),
) -> List[IPLookupResponse]:
    """
    Get provider and tag information for multiple IP addresses.
    Example: /api/v1/ips?ips=1.1.1.1&ips=8.8.8.8
    """
    try:
        return ip_service.lookup_multiple_ips(ips)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
