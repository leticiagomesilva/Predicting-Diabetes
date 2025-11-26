import boto3
from fastapi import UploadFile
from datetime import datetime
from app.config import settings


s3 = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_DEFAULT_REGION
)

BUCKET = settings.S3_BUCKET_NAME


def upload_to_s3(file: UploadFile):
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    object_name = f"{timestamp}_{file.filename}"

    s3.upload_fileobj(file.file, BUCKET, object_name)

    return object_name
