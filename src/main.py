import logging

from fastapi import FastAPI
from config.settings import settings
from exceptions.exception_handlers import register_exception_handlers
from controller.health_controller import router as health_router
from controller.storage_controller import router as storage_router
from controller.extraction_controller import router as extraction_router
from controller.retriever_controller import router as retriever_router

logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logging.getLogger("LiteLLM").setLevel(logging.ERROR)
logging.getLogger("LiteLLM Router").setLevel(logging.ERROR)
logging.getLogger("LiteLLM Proxy").setLevel(logging.ERROR)
app = FastAPI()
register_exception_handlers(app)
app.include_router(health_router)
app.include_router(storage_router)
app.include_router(extraction_router)
app.include_router(retriever_router)

@app.get("/")
def root():
    return {"status": "ok"}