import logging
import time

from ..document_indexing_context import DocumentIndexingContext

EMBEDDING_BATCH_SIZE = 128

logger = logging.getLogger(__name__)


class EmbedChunksStage:
    def __init__(self, embedding_engine, document_chunk_repository):
        self.embedding_engine = embedding_engine
        self.document_chunk_repository = document_chunk_repository

    async def process(self, ctx: DocumentIndexingContext) -> DocumentIndexingContext:
        started = time.perf_counter()
        for start in range(0, len(ctx.chunks), EMBEDDING_BATCH_SIZE):
            batch = ctx.chunks[start : start + EMBEDDING_BATCH_SIZE]
            embeddings = await self.embedding_engine.embed(
                [chunk.content for chunk in batch]
            )
            for chunk, embedding in zip(batch, embeddings, strict=True):
                chunk.embedding = embedding
            await self.document_chunk_repository.update_many(batch)
        logger.info(
            "Extraction %s embedded %d chunks in %.1fs",
            ctx.extraction_id,
            len(ctx.chunks),
            time.perf_counter() - started,
        )
        return ctx
