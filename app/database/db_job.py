""" File that encapsulates the ORM operations for the Job model """

from sqlalchemy.orm.session import Session
from database.database_models import SQLJob
from schemas.job import JobSchema


def create_job(job: JobSchema, db: Session):
    """ Function that creates a job in the database """
    job = SQLJob(**job.dict())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job