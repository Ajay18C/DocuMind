import logging
from uuid import uuid4

from fastapi.params import Depends
from model.extraction_model import Extraction
from repository.extraction_repository import get_extraction_repository
from service.storage.keys import safe_key
from service.storage_service import get_storage_service
from worker.extraction_worker import run_extraction_job

logger = logging.getLogger(__name__)


class ExtractionService:
    def __init__(self, extraction_repository, storage_service):
        self.extraction_repository = extraction_repository
        self.storage_service = storage_service

    async def start_extraction(self, data, filename, background_tasks):
        key = f"{uuid4().hex}_{safe_key(filename)}"
        await self.storage_service.save(data, key)
        extraction = Extraction(file_path=key)
        await self.extraction_repository.add(extraction)
        background_tasks.add_task(run_extraction_job, extraction.id, key, self.storage_service, filename)
        logger.info("Extraction %s scheduled for %s (key=%s)", extraction.id, filename, key)
        return {"detail": f"Extraction started for file: {filename}"}


def get_extraction_service(extraction_repository=Depends(get_extraction_repository), storage_service=Depends(get_storage_service)) -> ExtractionService:
    return ExtractionService(extraction_repository, storage_service)
