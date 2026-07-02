from fastapi import FastAPI
from controller.health_controller import router as health_router

app = FastAPI()
app.include_router(health_router)

@app.get("/")
def root():
    return {"status": "ok"}