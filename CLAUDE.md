# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

Package management is `uv`; tasks run through `poe` (poethepoet, dev dependency).

```bash
uv sync                                      # install dependencies
uv run poe dev                               # run the API (fastapi dev src/main.py)
uv run poe migrate                           # apply migrations (alembic upgrade head)
uv run alembic revision --autogenerate -m "" # create a migration
```

`DATABASE_URL` (Postgres, asyncpg) is required and read from `.env` at the repo root. There is no test suite yet.

Imports are rooted at `src/` with no package prefix (`from service.extraction_service import ...`), so ad-hoc scripts must run with `src` as the working directory: `cd src && uv run python -c "..."`.

## Commits

`<Type>: <imperative summary>` — e.g. `Add: Scanned PDF OCR via PaddleOCR`.

Types: `Add` (new capability), `Fix` (bug fix), `Refactor` (behavior-preserving restructure), `Docs` (docs only), `Chore` (deps, config, tooling), `Remove` (deleting code/features).

- Summary ≤ 72 chars, imperative mood, no trailing period.
- One concern per commit — split unrelated changes rather than combining types.
- Body only when the diff can't explain *why*; never restate what changed.

## Code style

This repo treats the code itself as the documentation: no comments (the rare exception is an external-system constraint, e.g. the asyncpg SSL note in `config/database.py`), intent-revealing names, one concept per file. Magic strings are enums (`ExtractionStatus`), and dead code is deleted, not kept.

## Architecture

Layered, with one-directional dependencies:

```
controller → service → worker → repository → model
```

A lower layer never imports from a higher one, and runtime callback cycles (A builds B which calls back into A) count as violations. Every layer wires dependencies through FastAPI `Depends` factory functions defined at the bottom of each module (`get_extraction_service`, `get_session`, ...); components receive collaborators via constructors and take the narrowest dependency that works (e.g. a pipeline stage takes a repository, never a whole service).

- **controller/** — HTTP translation only. Routers with Pydantic response models; domain exceptions are mapped to status codes by handlers registered in `exceptions/` via `register_exception_handlers(app)` in `main.py`.
- **service/** — orchestration. `ExtractionService.start_extraction` saves the upload to storage under a uuid-prefixed `safe_key` (collision- and traversal-safe), creates a `PENDING` row, and schedules the background job.
- **worker/** — background units of work. `worker/extraction_worker.py:run_extraction_job` owns the full job lifecycle: it opens its **own** DB session (`SessionLocal()` — never reuse a request-scoped session in a background task; FastAPI tears down yield-dependencies before background tasks run), re-reads the file from storage by key, marks the row `IN_PROGRESS`, runs the pipeline, and on any exception logs with the extraction id and persists `FAILED` with the error detail.
- **repository/** — persistence via generic `BaseRepository[T]` over an injected `AsyncSession`.
- **model/** — SQLModel tables; schema changes go through Alembic migrations in `migrations/versions/`.

### Worker pipeline (pipes-and-filters)

`worker/pipeline/` is a small framework: `Pipeline` runs a `Sequence[Stage]` where `Stage` is a `Protocol` (structural typing — implement `async def process(ctx) -> Context`, no inheritance) and all mutable state flows on a typed Pydantic `Context`. Stages are stateless; dependencies are injected at construction.

The extraction pipeline (`worker/pipeline/extraction/`) is assembled by the factory `build_extraction_pipeline(extraction_repository)`:

1. `DigitalDetectionStage` — extracts page texts **once** via the injected `PdfParser`, stores `ctx.page_texts`, classifies `ctx.pdf_type` (`PdfType` enum) Digital/Scanned.
2. `ExtractionRouterStage` — Strategy dispatch on `pdf_type`: `PdfType.DIGITAL` joins the already-extracted page texts; `PdfType.SCANNED` renders pages to images via the `PdfParser` and OCRs them (inline on the event loop — a deliberate trade-off). Adding a type means one new stage class plus one routing-dict entry. Unrouted types raise `UnsupportedPdfTypeError`, and an all-empty OCR result raises `EmptyOcrResultError` — both land the row in `FAILED` rather than a fake success.
3. `PersistExtractionStage` — writes `extraction_result` and `COMPLETED` through the repository.

The package is organized by concern: `stages/` (the five pipeline steps), `pdf/` (parsing seam), `ocr/` (OCR seam), with the context and pipeline factory at the package root.

PDF parsing and OCR are settings-selected seams for engine experiments, mirroring the storage pattern: `PdfParser` (`pdf/parser.py`) and `OcrEngine` (`ocr/engine.py`) are `Protocol`s with `@lru_cache` factories (`get_pdf_parser`, `get_ocr_engine`) that lazy-import the implementation chosen by `settings.PDF_PARSER` / `settings.OCR_ENGINE` (`pdf/pdfium_parser.py`, `ocr/paddle_engine.py` — PaddleOCR loads only when a scanned PDF is actually processed; first run downloads models to `~/.paddlex/official_models/`). Adding an engine: new implementation module + `Literal` member in settings + factory branch. Render DPI lives in `pdf/pdfium_parser.py:RENDER_SCALE`; OCR language in `settings.OCR_LANGUAGE`.

### Storage

`service/storage_service.py` wraps a `BaseStorage` backend chosen by `StorageFactory` from `settings.FILE_STORAGE` (`local` → `local_storage/` dir, `r2` → Cloudflare R2 via boto3; `R2_CONFIG` required when selected). All keys pass through `safe_key` (`service/storage/keys.py`), which rejects traversal and raises `UnsafeStorageKey` (mapped to HTTP 400).

### Config

`config/settings.py` is pydantic-settings over `.env`. `config/database.py` builds the async engine (asyncpg wants an `SSLContext`, not `?sslmode=require`) and exposes both `SessionLocal` (for workers) and the `get_session` yield dependency (for requests).
