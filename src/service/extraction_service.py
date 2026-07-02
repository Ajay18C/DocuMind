from fastapi.params import Depends
from functools import lru_cache
from model.extraction_model import Extraction
from repository.extraction_repository import get_extraction_repository
from service.storage_service import get_storage_service


class ExtractionService:
    def __init__(self, extraction_repository, storage_service):
        self.extraction_repository = extraction_repository
        self.storage_service = storage_service

    async def start_extraction(self, data, filename):
        print(f"Starting extraction for file: {filename}")
        await self.storage_service.save(data, filename)
        file_path = await self.storage_service.get_full_path(filename)
        await self.extraction_repository.add(Extraction(file_path=file_path))
        return {"detail": f"Extraction started for file: {filename}"}

@lru_cache
def get_extraction_service(extraction_repository=Depends(get_extraction_repository), storage_service=Depends(get_storage_service)) -> ExtractionService:
    return ExtractionService(extraction_repository, storage_service)
