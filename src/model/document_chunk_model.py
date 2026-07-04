from datetime import datetime, timezone

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, ForeignKey, Index, Integer
from sqlmodel import DateTime, Field, SQLModel


EMBEDDING_DIM = 1024


class DocumentChunk(SQLModel, table=True):
    __tablename__ = "document_chunk"

    id: int | None = Field(default=None, primary_key=True)
    extraction_id: int = Field(
        sa_column=Column(
            Integer,
            ForeignKey("extraction.id", ondelete="CASCADE"),
            index=True,
            nullable=False,
        )
    )
    chunk_index: int
    page_number: int
    content: str
    embedding: list[float] | None = Field(
        default=None, sa_column=Column(Vector(EMBEDDING_DIM), nullable=True)
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )

    __table_args__ = (
        Index(
            "ix_document_chunk_embedding_hnsw",
            "embedding",
            postgresql_using="hnsw",
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )