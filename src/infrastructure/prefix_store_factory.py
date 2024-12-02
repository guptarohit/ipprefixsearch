from pathlib import Path
import json
from typing import Type
from src.domain.models import IPPrefix
from src.infrastructure.prefix_store import AbstractPrefixStore


class PrefixStoreFactory:
    @staticmethod
    def create_from_json(
        store_class: Type[AbstractPrefixStore], json_path: Path
    ) -> AbstractPrefixStore:
        """
        Factory method to create and populate a prefix store from JSON data.

        Args:
            store_class: The class of the prefix store to create
            json_path: Path to the JSON file containing prefix data

        Returns:
            An initialized and populated prefix store
        """
        store = store_class()

        with open(json_path) as f:
            providers_data = json.load(f)
            for provider, provider_data in providers_data.items():
                for entry in provider_data:
                    tags = entry.get("tags", [])
                    for subnet in entry.get("prefixes", []):
                        prefix = IPPrefix(subnet=subnet, provider=provider, tags=tags)
                        store.add_prefix(prefix)

        return store
