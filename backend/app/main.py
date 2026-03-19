from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.settings import settings
from backend.api.consulta import router as consulta_router

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(consulta_router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "Juris AI MVP backend running",
        "environment": settings.app_env,
    }


@app.get("/health")
def health():
    return {"status": "ok"}
