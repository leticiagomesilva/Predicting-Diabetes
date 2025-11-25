from minio import Minio
from fastapi import UploadFile
from datetime import datetime
from app.config import settings


client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=False
)


def ensure_bucket():
    if not client.bucket_exists(settings.MINIO_BUCKET):
        client.make_bucket(settings.MINIO_BUCKET)


def upload_to_minio(file: UploadFile):
    ensure_bucket()

    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")
    object_name = f"{timestamp}_{file.filename}"

    client.put_object(
        bucket_name=settings.MINIO_BUCKET,
        object_name=object_name,
        data=file.file,
        length=-1,
        part_size=10 * 1024 * 1024,
    )

    return object_name
