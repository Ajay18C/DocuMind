from fastapi import APIRouter, BackgroundTasks, Depends, UploadFile, File
from pydantic import BaseModel
from service.extraction_service import get_extraction_service

router = APIRouter(
    prefix="/api", tags=["Extraction"]
)

class ExtractionResponse(BaseModel):
    detail: str

@router.post("/start_extraction", status_code=202, response_model=ExtractionResponse)
async def start_extraction(background_tasks: BackgroundTasks, file: UploadFile = File(...), extraction_service=Depends(get_extraction_service)):
    file_content = await file.read()
    result = await extraction_service.start_extraction(file_content, file.filename, background_tasks)
    return ExtractionResponse(**result)
