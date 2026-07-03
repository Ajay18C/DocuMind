from enum import Enum

from worker.pipeline.context import Context


class PdfType(str, Enum):
    DIGITAL = "Digital"
    SCANNED = "Scanned"
    UNKNOWN = "Unknown"


class ExtractionContext(Context):
    extraction_id: int
    pdf_content: bytes
    pdf_type: PdfType = PdfType.UNKNOWN
    page_texts: list[str] = []
    extracted_text: str = ""
