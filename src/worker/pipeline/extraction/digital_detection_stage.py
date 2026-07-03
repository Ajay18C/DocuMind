from .extraction_context import ExtractionContext
from .pdf_text import extract_page_texts


class DigitalDetectionStage:
    MIN_CHARS = 50

    async def process(self, ctx: ExtractionContext) -> ExtractionContext:
        ctx.page_texts = extract_page_texts(ctx.pdf_content)
        has_text = any(len(text.strip()) >= self.MIN_CHARS for text in ctx.page_texts)
        ctx.pdf_type = "Digital" if has_text else "Scanned"
        return ctx
