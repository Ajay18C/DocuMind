import pypdfium2 as pdfium


def extract_page_texts(pdf_content: bytes) -> list[str]:
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
