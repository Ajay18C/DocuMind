import asyncio
import logging
import time
from collections.abc import Callable

from worker.pipeline.page import Page

from ..extraction_context import ExtractionContext
from ..ocr.engine import OcrEngine
from ..pdf.parser import PdfParser

logger = logging.getLogger(__name__)


class EmptyOcrResultError(Exception):
    def __init__(self, page_count: int):
        super().__init__(f"OCR produced no text across {page_count} pages")
        self.page_count = page_count


class ScannedExtractionStage:
    def __init__(self, pdf_parser: PdfParser, ocr_engine_provider: Callable[[], OcrEngine]):
        self.pdf_parser = pdf_parser
        self.ocr_engine_provider = ocr_engine_provider

    async def process(self, ctx: ExtractionContext) -> ExtractionContext:
        logger.info("Extraction %s OCR started", ctx.extraction_id)
        started = time.perf_counter()
        texts = await asyncio.to_thread(self._ocr_pages, ctx.pdf_content)
        logger.info(
            "Extraction %s OCR finished: %d pages in %.1fs",
            ctx.extraction_id,
            len(texts),
            time.perf_counter() - started,
        )
        ctx.pages = [
            Page(page_number=number, text=text)
            for number, text in enumerate(texts, start=1)
        ]
        ctx.extracted_text = "\n".join(texts)
        if not ctx.extracted_text.strip():
            raise EmptyOcrResultError(len(texts))
        return ctx

    def _ocr_pages(self, pdf_content: bytes) -> list[str]:
        engine = self.ocr_engine_provider()
        return [
            "\n".join(engine.text_lines(image))
            for image in self.pdf_parser.page_images(pdf_content)
        ]
