import os
import tempfile

from app.database.database import SessionLocal
from app.repositories.job_repository import update_job_status
from app.services.invoice_service import process_invoice_file
from app.storage.storage_factory import get_storage
from app.utils.logger import get_logger


logger = get_logger(__name__)


class InvoiceWorker:

    def __init__(self, queue_service):
        self.queue_service = queue_service
        self.storage = get_storage()
        self.running = True

    def process_job(self, job: dict):

        job_id = job["job_id"]
        file_name = job["file_path"]
        extension = job["extension"]

        db = SessionLocal()
        downloaded_path = None

        try:
            logger.info(
                "Worker started job: %s",
                job_id
            )

            update_job_status(
                db,
                job_id,
                "processing"
            )

            # Download invoice from storage
            logger.info(
                "Downloading invoice from storage: %s",
                file_name
            )

            downloaded_path = self.storage.get(file_name)

            logger.info(
                "Invoice downloaded to: %s",
                downloaded_path
            )

            # Process invoice
            process_invoice_file(
                downloaded_path,
                extension,
                db
            )

            update_job_status(
                db,
                job_id,
                "completed"
            )

            logger.info(
                "Worker completed job: %s",
                job_id
            )

            return True

        except Exception as error:

            logger.exception(
                "Worker failed job: %s",
                job_id
            )

            update_job_status(
                db,
                job_id,
                "failed",
                str(error)
            )

            return False

        finally:

            db.close()

            # Remove downloaded temporary file
            if (
                downloaded_path
                and os.path.exists(downloaded_path)
            ):
                os.remove(downloaded_path)

    def run(self):

        logger.info("Invoice worker started")

        while self.running:

            job = self.queue_service.dequeue()

            # SQS can return None when there are no messages
            if job is None:
                continue

            try:

                success = self.process_job(job)

                # For SQS, delete message only after processing
                # LocalQueue simply marks the task as completed.
                if hasattr(
                    self.queue_service,
                    "task_done"
                ):
                    try:
                        self.queue_service.task_done(job)
                    except TypeError:
                        self.queue_service.task_done()

            except Exception:

                logger.exception(
                    "Unexpected worker error"
                )

    def stop(self):
        self.running = False


def start_worker(queue_service):

    worker = InvoiceWorker(queue_service)

    import threading

    thread = threading.Thread(
        target=worker.run,
        daemon=True
    )

    thread.start()

    return worker