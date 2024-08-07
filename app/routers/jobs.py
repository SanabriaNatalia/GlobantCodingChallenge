from fastapi import APIRouter, Depends
from schemas.job import JobSchema
from database import db_job
from sqlalchemy.orm.session import Session
from database.database_config import get_db
from typing import List

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def create_job(request : JobSchema, db: Session = Depends(get_db)):
    return db_job.create_job(request, db)

@router.post("/batch")
def create_job_batch(request: List[JobSchema], db: Session = Depends(get_db)):
    if not (1 <= len(request) <= 1000):
        raise HTTPException(status_code=400, detail="Batch size must be between 1 and 1000")
    successful_inserts, failed_inserts = db_job.create_job_batch(request, db)
    return {"successful_inserts": successful_inserts, "failed_inserts": failed_inserts}

@router.get("/all", response_model=List[JobSchema])
def get_all_jobs(db: Session = Depends(get_db)):
    return db_job.get_all_jobs(db)