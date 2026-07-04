from functools import lru_cache
from typing import Protocol

from config.settings import settings


class Chunker(Protocol):
    def chunk(self, text: str) -> list[str]: ...


@lru_cache
def get_chunker() -> Chunker:
    if settings.CHUNKER == "fixed":
        from .fixed_chunker import FixedChunker

        return FixedChunker(settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)
    raise ValueError(f"Unknown chunker: {settings.CHUNKER}")
