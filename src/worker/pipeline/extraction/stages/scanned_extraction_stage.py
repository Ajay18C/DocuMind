from collections.abc import Callable

from ..extraction_context import ExtractionContext
from ..ocr.engine import OcrEngine
from ..pdf.parser import PdfParser


class EmptyOcrResultError(Exception):
    def __init__(self, page_count: int):
        super().__init__(f"OCR produced no text across {page_count} pages")
        self.page_count = page_count


class ScannedExtractionStage:
    def __init__(self, pdf_parser: PdfParser, ocr_engine_provider: Callable[[], OcrEngine]):
        self.pdf_parser = pdf_parser
        self.ocr_engine_provider = ocr_engine_provider

    async def process(self, ctx: ExtractionContext) -> ExtractionContext:
        engine = self.ocr_engine_provider()
        ctx.page_texts = [
            "\n".join(engine.text_lines(image))
            for image in self.pdf_parser.page_images(ctx.pdf_content)
        ]
        ctx.extracted_text = "\n".join(ctx.page_texts)
        if not ctx.extracted_text.strip():
            raise EmptyOcrResultError(len(ctx.page_texts))
        return ctx
