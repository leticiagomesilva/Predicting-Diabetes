from fastapi import APIRouter, UploadFile, HTTPException
from app.services.s3_service import upload_to_s3

router = APIRouter()


@router.post("/upload")
async def upload_dataset(file: UploadFile):
    if not (file.filename.endswith(".csv") or file.filename.endswith(".json")):
        raise HTTPException(status_code=400, detail="File must be CSV or JSON.")

    object_name = upload_to_s3(file)

    return {"message": "File uploaded successfully", "object_name": object_name}