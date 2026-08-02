from functools import lru_cache
from typing import Protocol

from config.settings import settings
from enum import Enum

class ChunkStrategy(str, Enum):
    FIXED = "fixed"
    SEMANTIC = "semantic"


class Chunker(Protocol):
    def chunk(self, text: str) -> list[str]: ...


@lru_cache
def get_chunker() -> Chunker:
    if settings.CHUNKER == ChunkStrategy.FIXED:
        from .fixed_chunker import FixedChunker

        return FixedChunker(settings.CHUNK_SIZE, settings.CHUNK_OVERLAP)
    elif settings.CHUNKER == ChunkStrategy.SEMANTIC:
        from .semantic_chunker import SemChunker

        return SemChunker()
    raise ValueError(f"Unknown chunker: {settings.CHUNKER}")
