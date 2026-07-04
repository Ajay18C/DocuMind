from functools import lru_cache
from typing import Protocol

from config.settings import settings


class EmbeddingEngine(Protocol):
    async def embed(self, texts: list[str]) -> list[list[float]]: ...


@lru_cache
def get_embedding_engine() -> EmbeddingEngine:
    if settings.EMBEDDING_ENGINE == "voyage":
        from .voyage_engine import VoyageEmbeddingEngine

        return VoyageEmbeddingEngine(settings.VOYAGE_API_KEY)
    raise ValueError(f"Unknown embedding engine: {settings.EMBEDDING_ENGINE}")
