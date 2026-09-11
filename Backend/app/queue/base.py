from abc import ABC, abstractmethod


class QueueService(ABC):

    @abstractmethod
    def enqueue(self, job: dict) -> str:
        pass

    @abstractmethod
    def dequeue(self):
        pass