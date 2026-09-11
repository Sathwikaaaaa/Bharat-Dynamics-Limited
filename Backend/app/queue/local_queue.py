import queue

from app.utils.logger import get_logger

logger = get_logger(__name__)


class LocalQueue:

    def __init__(self):
        self.queue = queue.Queue()

    def enqueue(self, job: dict):
        self.queue.put(job)

        logger.info(
            "Job added to local queue: %s",
            job.get("job_id")
        )

    def dequeue(self):
        job = self.queue.get()

        logger.info(
            "Job removed from local queue: %s",
            job.get("job_id")
        )

        return job

    def task_done(self):
        self.queue.task_done()