import logging
import time

from config.database import SessionLocal
from model.extraction_model import ExtractionStatus
from repository.document_chunk_repository import DocumentChunkRepository
from repository.extraction_repository import ExtractionRepository
from worker.pipeline.document_indexing.document_indexing_context import (
    DocumentIndexingContext,
)
from worker.pipeline.document_indexing.document_indexing_pipeline import (
    build_document_indexing_pipeline,
)
from worker.pipeline.extraction.extraction_context import ExtractionContext
from worker.pipeline.extraction.extraction_pipeline import build_extraction_pipeline

logger = logging.getLogger(__name__)


async def run_extraction_job(extraction_id: int, file_path: str, storage_service) -> None:
    async with SessionLocal() as session:
        repository = ExtractionRepository(session)
        extraction = await repository.get(extraction_id)
        if extraction is None:
            logger.error("Extraction %s not found, skipping job", extraction_id)
            return
        extraction.status = ExtractionStatus.IN_PROGRESS
        await repository.update(extraction)
        logger.info("Extraction %s started (file=%s)", extraction_id, file_path)
        started = time.perf_counter()
        try:
            data = await storage_service.load(file_path)
            extraction_pipeline = build_extraction_pipeline(repository)
            extraction_ctx = await extraction_pipeline.run(
                ExtractionContext(extraction_id=extraction_id, pdf_content=data)
            )
            indexing_pipeline = build_document_indexing_pipeline(
                DocumentChunkRepository(session)
            )
            indexing_ctx = await indexing_pipeline.run(
                DocumentIndexingContext(
                    extraction_id=extraction_id,
                    pages=extraction_ctx.pages,
                )
            )
            extraction.status = ExtractionStatus.INDEXED
            await repository.update(extraction)
            logger.info(
                "Extraction %s indexed: %d chunks in %.1fs",
                extraction_id,
                len(indexing_ctx.chunks),
                time.perf_counter() - started,
            )
        except Exception as exc:
            logger.exception("Extraction %s failed", extraction_id)
            await session.rollback()
            extraction = await repository.get(extraction_id)
            extraction.status = ExtractionStatus.FAILED
            extraction.extraction_result = {
                **(extraction.extraction_result or {}),
                "error": str(exc),
            }
            await repository.update(extraction)
