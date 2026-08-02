import json
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

    async def build_context(self, data: str, extraction_id: int) -> str:
        context = await self.retriever.retrieve(data, extraction_id)
        return "".join([document_chunk[0].content for document_chunk in context])

    async def build_context_with_metadata(self, data: str, extraction_id: int) -> list:
        context = await self.retriever.retrieve(data, extraction_id)
        return [ f"<id>{con[0].id}</id><content>{con[0].content}</content>" for con in context], context

    async def build_system_prompt(self):
        return "You are a helpful assistant that provides accurate and concise answers based on the provided context. If the answer is not present in the context, you can think about it together with the context but you can't relate with the context with your own knowledge then respond with 'not found in documents.'"

    async def build_system_prompt_with_metadata(self):
        return """
        You are a helpful assistant that provides accurate and concise answers based on the provided context. If the answer is not present in the context, you can think about it together with the context but you can't relate with the context with your own knowledge then respond with 'not found in documents.' 
        The context is provided in the following format: <id>chunk_id</id><content>content</content>. 
        Return the citations array with the chunk_id that you used to answer the question. If the answer is not present in the context, respond with 'not found in documents. <reasoning>' along with the reasoning and return an empty citations array.

        # OUTPUT FORMAT
        {
            "answer": "Your answer here",
            "citations": ["chunk_id_1", "chunk_id_2"]
        }
        """

    async def build_user_prompt(self, question: str, context: str) -> str:
        return f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"

    async def build_user_prompt_with_metadata(self, question: str, context: list) -> str:
        context_str = "\n".join(context)
        return f"Context:\n{context_str}\n\nQuestion: {question}\nAnswer: ```JSON"

    async def get_similar_data(self, data: str, extraction_id: int) -> str:
        return await self.build_context(data, extraction_id)


    async def ask_question(self, question: str, extraction_id: int|None) -> str:
        context = await self.build_context(question, extraction_id)
        system_prompt = await self.build_system_prompt()
        user_prompt = await self.build_user_prompt(question, context)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        llm_response = await get_completion(messages)
        return llm_response.choices[0].message.content

    async def ask_question_with_metadata(self, question: str, extraction_id: int|None) -> str:
        context, context_with_metadata = await self.build_context_with_metadata(question, extraction_id)
        system_prompt = await self.build_system_prompt_with_metadata()
        user_prompt = await self.build_user_prompt_with_metadata(question, context)
        logger.info("System prompt: %s", system_prompt)
        logger.info("User prompt: %s", user_prompt)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        llm_response = await get_completion(messages, stop=["```"])
        logger.info("LLM response: %s", llm_response.choices[0].message.content)
        parsed_response = json.loads(llm_response.choices[0].message.content or "{}")
        logger.info("Parsed response: %s", parsed_response)
        llm_answer = parsed_response.get("answer", "not found in documents.")
        chunkids = parsed_response.get("citations", [])
        logger.info("Citations: %s", chunkids)
        citations = []
        for citation in chunkids:
            context_index = next((i for i, con in enumerate(context_with_metadata) if con[0].id == int(citation)), None)
            if context_index is not None:
                citations.append({"page_number": context_with_metadata[context_index][0].chunk_metadata.get("page_number", "unknown"), "filename": context_with_metadata[context_index][0].chunk_metadata.get("filename", "unknown")})

        return {"answer": llm_answer, "citations": citations}

def get_retriever_service(retriever = Depends(get_retriever())) -> RetrieverService:
    return RetrieverService(retriever)
