""" File that encapsulates the ORM operations for the Job model """

from sqlalchemy.orm.session import Session
from database.database_models import SQLJob
from schemas.job import JobSchema
from typing import List
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_job(job: JobSchema, db: Session):
    """ Function that creates a job in the database """
    job = SQLJob(**job.dict())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

def create_job_batch(jobs: List[JobSchema], db: Session):
    """ Function that creates a batch of jobs in the database """
    if not (1 <= len(jobs) <= 1000):
        raise ValueError("Batch size must be between 1 and 1000")

    successful_inserts = []
    failed_inserts = []

    for job in jobs:
        try:
            db_job = SQLJob(**job.dict())
            db.add(db_job)
            db.commit()
            db.refresh(db_job)
            successful_inserts.append(db_job)
            logger.info(f"Successfully inserted: {job.dict()}")
        except Exception as e:
            db.rollback()
            failed_inserts.append({"record": job.dict(), "error": str(e)})
            logger.error(f"Failed to insert: {job.dict()} with error: {str(e)}")
    
    return successful_inserts, failed_inserts

def get_all_jobs(db: Session):
    """ Function that retrieves all jobs from the database """
    return db.query(SQLJob).all()

def get_job_by_id(job_id: int, db: Session):
    """ Function that retrieves a job by its ID """
    return db.query(SQLJob).filter(SQLJob.id == job_id).first()

def update_job(job_id: int, job: JobSchema, db: Session):
    """ Function that updates a job by its ID """
    job = db.query(SQLJob).filter(SQLJob.id == job_id)
    job.update(**job.dict())
    db.commit()
    return job.first()

def delete_job(job_id: int, db: Session):
    """ Function that deletes a job by its ID """
    job = db.query(SQLJob).filter(SQLJob.id == job_id)
    job.delete()
    db.commit()
    return job.first()
