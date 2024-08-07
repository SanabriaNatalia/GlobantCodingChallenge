from fastapi import APIRouter, Depends, HTTPException, status
from schemas.department import DepartmentSchema
from database import db_department
from sqlalchemy.orm import Session
from database.database_config import get_db
from typing import List

router = APIRouter(
    prefix="/departments",
    tags=["departments"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def create_department(request : DepartmentSchema, db: Session = Depends(get_db)):
    return db_department.create_department(request, db)

@router.post("/batch")
def create_department_batch(request: List[DepartmentSchema], db: Session = Depends(get_db)):
    if not (1 <= len(request) <= 1000):
        raise HTTPException(status_code=400, detail="Batch size must be between 1 and 1000")
    successful_inserts, failed_inserts = db_department.create_department_batch(request, db)
    return {"successful_inserts": successful_inserts, "failed_inserts": failed_inserts}

@router.get("/all", response_model=List[DepartmentSchema])
def get_all_departments(db: Session = Depends(get_db)):
    return db_department.get_all_departments(db)
