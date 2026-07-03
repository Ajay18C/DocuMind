from functools import lru_cache
from typing import Protocol

import numpy as np

from config.settings import settings


class PdfParser(Protocol):
    def page_texts(self, pdf_content: bytes) -> list[str]: ...

    def page_images(self, pdf_content: bytes) -> list[np.ndarray]: ...


@lru_cache
def get_pdf_parser() -> PdfParser:
    if settings.PDF_PARSER == "pdfium":
        from .pdfium_parser import PdfiumParser

        return PdfiumParser()
    raise ValueError(f"Unknown pdf parser: {settings.PDF_PARSER}")
