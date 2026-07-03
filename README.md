# Documind

## Stack

**Backend** : FastApi
**Database**: Postgres
**FileStorage**: Cloudflare R2 via boto3
**Workers**: FastApi backgroundjob
**OCR**:
    - **Digital** : pypdfium2
    - **Scanned** : PaddleOCR (PP-OCRv5, local); ocr.space planned


## Background Job

### Extraction
    - detect Digital vs Scanned from extractable text
    - Digital: pypdfium2 page texts joined and persisted
    - Scanned: pages rendered to images, PaddleOCR text persisted
    - empty OCR result or unrouted type fails the row
