from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from model.document_chunk_model import DocumentChunk
from repository.base_repository import BaseRepository
from fastapi import Depends
from config.database import get_session


class DocumentChunkRepository(BaseRepository[DocumentChunk]):
    def __init__(self, session:AsyncSession):
        super().__init__(DocumentChunk, session)

    async def search_similar(
        self,
        query_embedding: list[float],
        limit: int = 5,
        extraction_id: int | None = None,
    ) -> list[tuple[DocumentChunk, float]]:
        distance = DocumentChunk.embedding.cosine_distance(query_embedding)
        stmt = select(DocumentChunk, distance.label("distance")).where(
            DocumentChunk.embedding.is_not(None)
        )

        if extraction_id is not None:
            stmt = stmt.where(DocumentChunk.extraction_id == extraction_id)

        stmt = stmt.order_by(distance).limit(limit)
        result = await self.session.execute(stmt)
        return [(row[0], row[1]) for row in result.all()]

def get_document_chunk_repository(db = Depends(get_session)) -> DocumentChunkRepository:
    return DocumentChunkRepository(db)