"""Central source registry module for verifiable citations and regulatory provenance."""

from src.registry.sources import (
    SOURCE_REGISTRY,
    SourceEntry,
    get_source_registry,
    get_sources_by_type,
)

__all__ = [
    "SOURCE_REGISTRY",
    "SourceEntry",
    "get_source_registry",
    "get_sources_by_type",
]
