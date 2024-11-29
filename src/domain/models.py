from pydantic import BaseModel
from typing import List


class IPPrefix(BaseModel):
    subnet: str
    provider: str
    tags: List[str]


class IPLookupResult(BaseModel):
    subnet: str
    provider: str
    tags: List[str]


class IPLookupResponse(BaseModel):
    result: List[IPLookupResult]
