from functools import lru_cache
from typing import Protocol

import numpy as np

from config.settings import settings


class OcrEngine(Protocol):
    def text_lines(self, image: np.ndarray) -> list[str]: ...


@lru_cache
def get_ocr_engine() -> OcrEngine:
    if settings.OCR_ENGINE == "paddle":
        from .paddle_engine import PaddleOcrEngine

        return PaddleOcrEngine(settings.OCR_LANGUAGE)
    raise ValueError(f"Unknown ocr engine: {settings.OCR_ENGINE}")
