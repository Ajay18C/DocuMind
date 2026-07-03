import logging

from config.database import SessionLocal
from model.extraction_model import ExtractionStatus
from repository.extraction_repository import ExtractionRepository
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
        try:
            data = await storage_service.load(file_path)
            pipeline = build_extraction_pipeline(repository)
            await pipeline.run(
                ExtractionContext(extraction_id=extraction_id, pdf_content=data)
            )
        except Exception as exc:
            logger.exception("Extraction %s failed", extraction_id)
            await session.rollback()
            extraction.status = ExtractionStatus.FAILED
            extraction.extraction_result = {"error": str(exc)}
            await repository.update(extraction)
