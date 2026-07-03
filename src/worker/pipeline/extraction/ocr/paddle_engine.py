import numpy as np
from paddleocr import PaddleOCR


class PaddleOcrEngine:
    def __init__(self, language: str):
        self.paddle_ocr = PaddleOCR(
            lang=language,
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
        )

    def text_lines(self, image: np.ndarray) -> list[str]:
        result = self.paddle_ocr.predict(image)
        return list(result[0]["rec_texts"])
