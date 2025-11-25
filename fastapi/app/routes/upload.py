from fastapi import APIRouter, UploadFile, HTTPException
from app.services.minio_service import upload_to_minio

router = APIRouter()


@router.post("/upload")
async def upload_dataset(file: UploadFile):
    if not file.filename.endswith(".csv") and not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="File must be CSV or JSON.")

    object_name = upload_to_minio(file)

    return {"message": "File uploaded successfully", "object_name": object_name}
