from fastapi import FastAPI
from backend.core.settings import settings

app = FastAPI(title=settings.app_name)

@app.get("/")
def root():
    return {
        "message": "Juris AI MVP backend running",
        "environment": settings.app_env,
    }

@app.get("/health")
def health():
    return {"status": "ok"}
