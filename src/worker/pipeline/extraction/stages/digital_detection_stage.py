from ..extraction_context import ExtractionContext, PdfType
from ..pdf.parser import PdfParser


class DigitalDetectionStage:
    MIN_CHARS = 50

    def __init__(self, pdf_parser: PdfParser):
        self.pdf_parser = pdf_parser

    async def process(self, ctx: ExtractionContext) -> ExtractionContext:
        ctx.page_texts = self.pdf_parser.page_texts(ctx.pdf_content)
        has_text = any(len(text.strip()) >= self.MIN_CHARS for text in ctx.page_texts)
        ctx.pdf_type = PdfType.DIGITAL if has_text else PdfType.SCANNED
        return ctx
