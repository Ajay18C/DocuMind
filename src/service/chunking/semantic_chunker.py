from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()

class SemChunker:
    def __init__(self):
        self.chunker = SemanticChunker(
            embeddings=OpenAIEmbeddings(
                model="openai/text-embedding-3-small",
                api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1",
                check_embedding_ctx_length=False,
            ),
            breakpoint_threshold_type="percentile",
            breakpoint_threshold_amount=90,
        )

    def chunk(self, text: str) -> list[str]:
        chunks = self.chunker.split_text(text)
        return chunks

