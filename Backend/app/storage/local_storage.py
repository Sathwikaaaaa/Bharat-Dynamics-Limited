import os
import shutil

from app.storage.base import StorageService


class LocalStorage(StorageService):

    def __init__(self, base_dir: str = "storage"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def save(
        self,
        file_path: str,
        destination_name: str
    ) -> str:

        destination_path = os.path.join(
            self.base_dir,
            destination_name
        )

        shutil.copy2(
            file_path,
            destination_path
        )

        return destination_path

    def get(self, file_name: str) -> str:

        file_path = os.path.join(
            self.base_dir,
            file_name
        )

        if not os.path.exists(file_path):
            raise FileNotFoundError(
                f"File not found: {file_name}"
            )

        return file_path

    def delete(self, file_name: str) -> None:

        file_path = os.path.join(
            self.base_dir,
            file_name
        )

        if os.path.exists(file_path):
            os.remove(file_path)