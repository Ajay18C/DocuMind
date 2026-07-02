from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from service.storage.keys import UnsafeStorageKey


async def _unsafe_storage_key_handler(request: Request, exc: UnsafeStorageKey):
    return JSONResponse(status_code=400, content={"detail": "Invalid filename."})


async def _file_not_found_handler(request: Request, exc: FileNotFoundError):
    return JSONResponse(status_code=404, content={"detail": "File not found."})


def register_exception_handlers(app: FastAPI) -> None:
    """Map storage-layer exceptions to HTTP responses, app-wide."""
    app.add_exception_handler(UnsafeStorageKey, _unsafe_storage_key_handler)
    app.add_exception_handler(FileNotFoundError, _file_not_found_handler)
