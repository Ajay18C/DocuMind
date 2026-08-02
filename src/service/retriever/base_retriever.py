from functools import lru_cache
from typing import Protocol
from config.settings import settings


class BaseRetriever(Protocol):
    def retrieve(self, data: str, extraction_id: int) -> list:
        ...

@lru_cache
def get_retriever() -> BaseRetriever:
    if settings.RETRIEVER == "topk":
        from .topk_retriever import get_topk_retriever
        return get_topk_retriever
    raise ValueError(f"Unknown embedding engine: {settings.RETRIEVER}")