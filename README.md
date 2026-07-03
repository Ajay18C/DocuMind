# Documind

## Stack

**Backend** : FastApi
**Database**: Postgres
**FileStorage**: Cloudflare R2 via boto3
**Workers**: FastApi backgroundjob
**OCR**:
    - **Digital** : pdfplumber
    - **Scanned** : Paddle ocr, ocr.space


## Background Job

### Extraction
    - digital check
    - for digital use pdfplumer get all data and accumulte in a string and persist in db
