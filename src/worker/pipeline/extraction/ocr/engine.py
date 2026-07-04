import logging
import time
from functools import lru_cache
from typing import Protocol

import numpy as np

from config.settings import settings

logger = logging.getLogger(__name__)


class OcrEngine(Protocol):
    def text_lines(self, image: np.ndarray) -> list[str]: ...


@lru_cache
def get_ocr_engine() -> OcrEngine:
    if settings.OCR_ENGINE == "paddle":
        from .paddle_engine import PaddleOcrEngine

        logger.info("Loading OCR engine %s (language=%s)", settings.OCR_ENGINE, settings.OCR_LANGUAGE)
        started = time.perf_counter()
        engine = PaddleOcrEngine(settings.OCR_LANGUAGE)
        logger.info("OCR engine ready in %.1fs", time.perf_counter() - started)
        return engine
    raise ValueError(f"Unknown ocr engine: {settings.OCR_ENGINE}")
