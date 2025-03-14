"""Upload image to Cloudflare R2"""

import boto3
from botocore.client import Config

class Upload:
    """Upload image to Cloudflare R2"""

    def __init__(self, endpoint_url: str, access_key: str, secret_key: str):
        self.client = boto3.client(
            's3',
            endpoint_url=endpoint_url,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=Config(signature_version='s3v4')
        )

    def upload(self, bucket_name: str, object_key: str, file_path: str):
        """Upload image to Cloudflare R2"""
        print("START UPLOAD IMAGE...")
        with open(file_path, 'rb') as file:
            self.client.upload_fileobj(file, bucket_name, object_key)
        print(f"FINISH UPLOAD IMAGE FROM {file_path} TO {bucket_name}/{object_key}!")
