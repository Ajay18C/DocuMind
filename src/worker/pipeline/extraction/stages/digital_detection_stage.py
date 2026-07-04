import asyncio
import logging

from worker.pipeline.page import Page

from ..extraction_context import ExtractionContext, PdfType
from ..pdf.parser import PdfParser

logger = logging.getLogger(__name__)


class DigitalDetectionStage:
    MIN_CHARS = 50

    def __init__(self, pdf_parser: PdfParser):
        self.pdf_parser = pdf_parser

    async def process(self, ctx: ExtractionContext) -> ExtractionContext:
        texts = await asyncio.to_thread(self.pdf_parser.page_texts, ctx.pdf_content)
        ctx.pages = [
            Page(page_number=number, text=text)
            for number, text in enumerate(texts, start=1)
        ]
        has_text = any(len(page.text.strip()) >= self.MIN_CHARS for page in ctx.pages)
        ctx.pdf_type = PdfType.DIGITAL if has_text else PdfType.SCANNED
        logger.info(
            "Extraction %s classified as %s (%d pages, max page chars=%d)",
            ctx.extraction_id,
            ctx.pdf_type.value,
            len(ctx.pages),
            max((len(page.text.strip()) for page in ctx.pages), default=0),
        )
        return ctx
