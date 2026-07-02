from fastapi import APIRouter, Depends, UploadFile, File, Response
from pydantic import BaseModel
from service.storage_service import get_storage_service

router = APIRouter(
    prefix="/api", tags=["Storage"]
)

class UploadResponse(BaseModel):
    filename: str
    size: int
    url: str

@router.post("/upload", status_code=201, response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...), storage_service=Depends(get_storage_service)):
    file_content = await file.read()
    await storage_service.save(file_content, file.filename)
    return UploadResponse(
        filename=file.filename,
        size=len(file_content),
        url=f"/api/files/{file.filename}"
    )

@router.get("/files/{filename}")
async def get_file(filename: str, storage_service=Depends(get_storage_service)):
    file_content = await storage_service.load(filename)
    return Response(content=file_content, media_type="application/octet-stream")


@router.delete("/files/{filename}", status_code=204)
async def delete_file(filename: str, storage_service=Depends(get_storage_service)):
    await storage_service.delete(filename)

@router.get("/files/{filename}/url", response_model=str)
async def get_file_url(filename: str, storage_service=Depends(get_storage_service)):
    return await storage_service.get_public_url(filename)
