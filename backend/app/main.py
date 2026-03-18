from fastapi import FastAPI

app = FastAPI(title="Juris AI MVP Backend")

@app.get("/")
def root():
    return {"message": "Juris AI MVP backend running"}

@app.get("/health")
def health():
    return {"status": "ok"}
