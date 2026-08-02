from fastapi import APIRouter, Depends
from service.retriever_service import get_retriever_service

router = APIRouter(
    prefix="/api", tags=["Retriever"]
)

@router.post("/retrieve_data", status_code=200)
async def retrieve_data(data: str, extraction_id: int, retriever_service=Depends(get_retriever_service)) -> str:
    return await retriever_service.get_similar_data(data, extraction_id)

@router.post("/ask_question", status_code=200)
async def ask_question(question: str, extraction_id: int|None=None, retriever_service=Depends(get_retriever_service)) -> str:
    return await retriever_service.ask_question(question, extraction_id)

@router.post("/ask_question_with_metadata", status_code=200)
async def ask_question_with_metadata(question: str, extraction_id: int|None=None, retriever_service=Depends(get_retriever_service)) -> dict:
    return await retriever_service.ask_question_with_metadata(question, extraction_id)