import os

from app.queue.local_queue import LocalQueue
from app.queue.sqs_queue import SQSQueue


def get_queue():

    queue_type = os.getenv(
        "QUEUE_TYPE",
        "local"
    ).lower()

    if queue_type == "sqs":
        return SQSQueue()

    return LocalQueue()