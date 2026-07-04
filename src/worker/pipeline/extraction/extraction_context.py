from enum import Enum

from worker.pipeline.context import Context
from worker.pipeline.page import Page


class PdfType(str, Enum):
    DIGITAL = "Digital"
    SCANNED = "Scanned"
    UNKNOWN = "Unknown"


class ExtractionContext(Context):
    extraction_id: int
    pdf_content: bytes
    pdf_type: PdfType = PdfType.UNKNOWN
    pages: list[Page] = []
    extracted_text: str = ""
