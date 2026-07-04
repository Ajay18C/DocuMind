from model.document_chunk_model import DocumentChunk

from ..document_indexing_context import DocumentIndexingContext


class EmptyExtractedTextError(Exception):
    def __init__(self, extraction_id: int):
        super().__init__(f"Extraction {extraction_id} produced no chunkable text")


class ChunkTextStage:
    def __init__(self, chunker):
        self.chunker = chunker

    async def process(self, ctx: DocumentIndexingContext) -> DocumentIndexingContext:
        chunks = []
        for page in ctx.pages:
            for content in self.chunker.chunk(page.text):
                chunks.append(
                    DocumentChunk(
                        extraction_id=ctx.extraction_id,
                        chunk_index=len(chunks),
                        page_number=page.page_number,
                        content=content,
                    )
                )
        if not chunks:
            raise EmptyExtractedTextError(ctx.extraction_id)
        ctx.chunks = chunks
        return ctx
