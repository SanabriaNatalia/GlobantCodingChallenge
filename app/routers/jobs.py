from fastapi import APIRouter, Depends
from schemas.job import JobSchema
from database import db_job
from sqlalchemy.orm.session import Session
from database.database_config import get_db

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def create_job(request : JobSchema, db: Session = Depends(get_db)):
    return db_job.create_job(request, db)