import logging
from pyexpat.errors import messages
from uuid import uuid4

from fastapi import Depends
from service.retriever.base_retriever import get_retriever
from service.llm.litellm import get_completion

logger = logging.getLogger(__name__)


class RetrieverService:
    def __init__(self, retriever):
        self.retriever = retriever

    async def get_similar_data(self, data: str, extraction_id: int) -> str:
        context = await self.retriever.retrieve(data, extraction_id)
        return "".join([document_chunk[0].content for document_chunk in context])


    async def ask_question(self, question: str, extraction_id: int|None) -> str:
        context = await self.retriever.retrieve(question, extraction_id=extraction_id)
        system_prompt = "You are a helpful assistant that provides accurate and concise answers based on the provided context. If the answer is not present in the context, respond with 'not found in documents.'"
        user_prompt = f"Context:\n{''.join([document_chunk[0].content for document_chunk in context])}\n\nQuestion: {question}\nAnswer:"
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        llm_response = await get_completion(messages)
        return llm_response.choices[0].message.content

def get_retriever_service(retriever = Depends(get_retriever())) -> RetrieverService:
    return RetrieverService(retriever)
