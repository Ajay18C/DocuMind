import logging

from ..document_indexing_context import DocumentIndexingContext

logger = logging.getLogger(__name__)


class PersistChunksStage:
    def __init__(self, document_chunk_repository):
        self.document_chunk_repository = document_chunk_repository

    async def process(self, ctx: DocumentIndexingContext) -> DocumentIndexingContext:
        await self.document_chunk_repository.add_many(ctx.chunks)
        logger.info(
            "Extraction %s persisted %d chunks awaiting embedding",
            ctx.extraction_id,
            len(ctx.chunks),
        )
        return ctx
