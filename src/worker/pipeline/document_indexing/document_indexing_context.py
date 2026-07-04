from model.document_chunk_model import DocumentChunk
from worker.pipeline.context import Context
from worker.pipeline.page import Page


class DocumentIndexingContext(Context):
    extraction_id: int
    pages: list[Page] = []
    chunks: list[DocumentChunk] = []
