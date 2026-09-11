from abc import ABC, abstractmethod


class StorageService(ABC):

    @abstractmethod
    def save(self, file_path: str, destination_name: str) -> str:
        pass

    @abstractmethod
    def get(self, file_name: str) -> str:
        pass

    @abstractmethod
    def delete(self, file_name: str) -> None:
        pass