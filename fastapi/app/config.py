from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    AWS_ACCESS_KEY_ID: str
    AWS_SECRET_ACCESS_KEY: str
    AWS_DEFAULT_REGION: str = "us-east-2"
    S3_BUCKET_NAME: str

    model_config = {
        "env_file": ".env"
    }

settings = Settings()