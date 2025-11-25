from fastapi import FastAPI
from app.routes.upload import router as upload_router

app = FastAPI(title="Diabetes Ingestion API")

@app.get("/")
def root():
    return {"status": "running"}

app.include_router(upload_router, prefix="/api")
