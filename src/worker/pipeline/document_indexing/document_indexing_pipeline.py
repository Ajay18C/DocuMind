from worker.pipeline.pipeline import Pipeline

from .chunking.chunker import get_chunker
from .embedding.engine import get_embedding_engine
from .stages.chunk_text_stage import ChunkTextStage
from .stages.embed_chunks_stage import EmbedChunksStage
from .stages.persist_chunks_stage import PersistChunksStage


def build_document_indexing_pipeline(document_chunk_repository) -> Pipeline:
    return Pipeline(
        [
            ChunkTextStage(get_chunker()),
            PersistChunksStage(document_chunk_repository),
            EmbedChunksStage(get_embedding_engine(), document_chunk_repository),
        ]
    )
