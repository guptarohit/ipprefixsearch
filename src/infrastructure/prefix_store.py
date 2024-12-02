from abc import ABC, abstractmethod
from typing import List
from src.domain.models import IPPrefix


class AbstractPrefixStore(ABC):
    @abstractmethod
    def add_prefix(self, prefix: IPPrefix) -> None:
        pass

    @abstractmethod
    def lookup_ip(self, ip: str) -> List[IPPrefix]:
        pass
