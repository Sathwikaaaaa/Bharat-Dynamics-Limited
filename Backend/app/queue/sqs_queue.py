import json
import os

import boto3

from app.utils.logger import get_logger


logger = get_logger(__name__)


class SQSQueue:

    def __init__(self):
        self.queue_url = os.getenv("SQS_QUEUE_URL")
        self.region = os.getenv("AWS_REGION", "ap-south-2")

        if not self.queue_url:
            raise RuntimeError(
                "SQS_QUEUE_URL is not configured."
            )

        self.sqs = boto3.client(
            "sqs",
            region_name=self.region
        )

    def enqueue(self, job: dict):

        response = self.sqs.send_message(
            QueueUrl=self.queue_url,
            MessageBody=json.dumps(job)
        )

        logger.info(
            "Job added to SQS: %s",
            job.get("job_id")
        )

        return response["MessageId"]

    def dequeue(self):

        response = self.sqs.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20
        )

        messages = response.get("Messages", [])

        if not messages:
            return None

        message = messages[0]

        job = json.loads(message["Body"])

        job["_receipt_handle"] = message["ReceiptHandle"]

        logger.info(
            "Job received from SQS: %s",
            job.get("job_id")
        )

        return job

    def task_done(self, job):

        receipt_handle = job.get("_receipt_handle")

        if receipt_handle:
            self.sqs.delete_message(
                QueueUrl=self.queue_url,
                ReceiptHandle=receipt_handle
            )

            logger.info(
                "Job removed from SQS: %s",
                job.get("job_id")
            )