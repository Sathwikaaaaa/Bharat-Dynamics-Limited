from sqlalchemy.orm import Session

from app.database.models import Job


def create_job(
    db: Session,
    job_id: str,
    file_name: str,
    file_path: str
):
    job = Job(
        job_id=job_id,
        file_name=file_name,
        file_path=file_path,
        status="queued"
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


def get_job(db: Session, job_id: str):
    return (
        db.query(Job)
        .filter(Job.job_id == job_id)
        .first()
    )


def update_job_status(
    db: Session,
    job_id: str,
    status: str,
    error_message: str = None,
    invoice_id: int = None
):
    job = get_job(db, job_id)

    if not job:
        return None

    job.status = status
    job.error_message = error_message

    if invoice_id is not None:
        job.invoice_id = invoice_id

    db.commit()
    db.refresh(job)

    return job