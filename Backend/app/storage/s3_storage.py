import os
import tempfile

import boto3

from app.storage.base import StorageService


class S3Storage(StorageService):

    def __init__(self):
        self.bucket_name = os.getenv("S3_BUCKET_NAME")
        self.region = os.getenv("AWS_REGION", "ap-south-1")

        if not self.bucket_name:
            raise RuntimeError("S3_BUCKET_NAME is not configured.")

        self.s3 = boto3.client(
            "s3",
            region_name=self.region
        )

    def save(self, file_path, destination_name):
        self.s3.upload_file(
            file_path,
            self.bucket_name,
            destination_name
        )

        return f"s3://{self.bucket_name}/{destination_name}"

    def get(self, file_name):
        suffix = os.path.splitext(file_name)[1]

        temporary_file = tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        )

        temporary_file.close()

        self.s3.download_file(
            self.bucket_name,
            file_name,
            temporary_file.name
        )

        return temporary_file.name

    def delete(self, file_name):
        self.s3.delete_object(
            Bucket=self.bucket_name,
            Key=file_name
        )