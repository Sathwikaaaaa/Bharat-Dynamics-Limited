import os

from app.storage.local_storage import LocalStorage
from app.storage.s3_storage import S3Storage


def get_storage():

    storage_type = os.getenv(
        "STORAGE_TYPE",
        "local"
    ).lower()

    if storage_type == "s3":
        return S3Storage()

    return LocalStorage()