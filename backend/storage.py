import os
from pathlib import Path
from typing import Optional

USE_S3 = os.getenv("USE_S3", "0") == "1"
S3_BUCKET = os.getenv("S3_BUCKET", "")
S3_PREFIX = os.getenv("S3_PREFIX", "gen/")
S3_REGION = os.getenv("AWS_REGION", "ap-south-1")

def local_output_dir() -> Path:
    return Path(__file__).parent / "output"

def upload_s3_if_enabled(local_path: str) -> Optional[str]:
    """
    If USE_S3=1 and AWS creds are set in env, upload file to S3 and return its URL.
    Otherwise return None and the API will serve local /download link.
    """
    if not USE_S3:
        return None
    import boto3
    from botocore.config import Config
    s3 = boto3.client("s3", region_name=S3_REGION, config=Config(signature_version="s3v4"))
    key = S3_PREFIX + Path(local_path).name
    s3.upload_file(local_path, S3_BUCKET, key, ExtraArgs={"ContentType": "model/stl"})
    return f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{key}"
