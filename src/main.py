from fastapi import FastAPI
from exceptions.exception_handlers import register_exception_handlers
from controller.health_controller import router as health_router
from controller.storage_controller import router as storage_router
from controller.extraction_controller import router as extraction_router

app = FastAPI()
register_exception_handlers(app)
app.include_router(health_router)
app.include_router(storage_router)
app.include_router(extraction_router)

@app.get("/")
def root():
    return {"status": "ok"}