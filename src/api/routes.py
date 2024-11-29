from fastapi import APIRouter, HTTPException
from typing import List
from src.domain.models import IPLookupResponse
from src.services.ip_lookup_service import IPLookupService
from src.infrastructure.prefix_store import PrefixStore
from pathlib import Path

router = APIRouter()

# Get the project root directory
project_root = Path(__file__).parent.parent.parent
json_path = project_root / "prefixes.json"

prefix_store = PrefixStore.from_json(json_path)
ip_service = IPLookupService(prefix_store)


@router.get("/lookup/{ip}", response_model=IPLookupResponse)
async def lookup_single_ip(ip: str) -> IPLookupResponse:
    try:
        return ip_service.lookup_single_ip(ip)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/lookup/batch", response_model=List[IPLookupResponse])
async def lookup_multiple_ips(ips: List[str]) -> List[IPLookupResponse]:
    try:
        return ip_service.lookup_multiple_ips(ips)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
