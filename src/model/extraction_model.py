from datetime import datetime, timezone
from enum import Enum

from sqlmodel import DateTime, SQLModel, Field
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB


class ExtractionStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    INDEXED = "indexed"
    FAILED = "failed"


class Extraction(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    file_path: str
    status: ExtractionStatus = Field(default=ExtractionStatus.PENDING)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True), onupdate=lambda: datetime.now(timezone.utc)),
    )
    extraction_result: dict = Field(
        default_factory=dict,
        sa_column=Column(JSONB),
    )