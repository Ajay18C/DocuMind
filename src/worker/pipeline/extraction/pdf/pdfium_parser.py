import numpy as np
import pypdfium2 as pdfium

RENDER_SCALE = 2.0


class PdfiumParser:
    def page_texts(self, pdf_content: bytes) -> list[str]:
        pdf = pdfium.PdfDocument(pdf_content)
        try:
            texts = []
            for page in pdf:
                textpage = page.get_textpage()
                texts.append(textpage.get_text_bounded())
                textpage.close()
                page.close()
            return texts
        finally:
            pdf.close()

    def page_images(self, pdf_content: bytes) -> list[np.ndarray]:
        pdf = pdfium.PdfDocument(pdf_content)
        try:
            images = []
            for page in pdf:
                bitmap = page.render(scale=RENDER_SCALE)
                images.append(bitmap.to_numpy()[:, :, :3])
                page.close()
            return images
        finally:
            pdf.close()
