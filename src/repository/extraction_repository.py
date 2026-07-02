from fastapi import Depends

from config.database import get_session
from model.extraction_model import Extraction
from repository.base_repository import BaseRepository


class ExtractionRepository(
    BaseRepository[Extraction]
):
    def __init__(self, db):
        super().__init__(Extraction, db)

def get_extraction_repository(
    db = Depends(get_session),
) -> ExtractionRepository:
    return ExtractionRepository(db)
