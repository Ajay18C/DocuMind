from fastapi import Depends
from repository.document_chunk_repository import get_document_chunk_repository
from service.embedding.engine import get_embedding_engine


class TopkRetriever:
    def __init__(self, document_chunk_repository, embedding_engine):
        self.document_chunk_repository = document_chunk_repository
        self.embedding_engine = embedding_engine

    async def retrieve(self, data: str, extraction_id: int) -> list:
        embeddings = await self.embedding_engine.embed([data])
        return await self.document_chunk_repository.search_similar(embeddings[0], extraction_id= extraction_id, limit=5)

def get_topk_retriever(document_chunk_repository=Depends(get_document_chunk_repository), embedding_engine=Depends(get_embedding_engine)):
    return TopkRetriever(document_chunk_repository, embedding_engine)