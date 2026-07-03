from worker.pipeline.context import Context


class ExtractionContext(Context):
    extraction_id: int
    pdf_content: bytes
    pdf_type: str = "Unknown"
    page_texts: list[str] = []
    extracted_text: str = ""
