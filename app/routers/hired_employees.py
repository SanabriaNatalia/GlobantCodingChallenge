from fastapi import APIRouter, Depends
from schemas.hired_employee import HiredEmployeeSchema
from database import db_hired_employee
from sqlalchemy.orm.session import Session
from database.database_config import get_db
from typing import List

router = APIRouter(
    prefix="/hired_employees",
    tags=["hired_employees"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def create_hired_employee(request : HiredEmployeeSchema, db: Session = Depends(get_db)):
    return db_hired_employee.create_hired_employee(request, db)

@router.post("/batch")
def create_hired_employee_batch(request: List[HiredEmployeeSchema], db: Session = Depends(get_db)):
    if not (1 <= len(request) <= 1000):
        raise HTTPException(status_code=400, detail="Batch size must be between 1 and 1000")
    successful_inserts, failed_inserts = db_hired_employee.create_hired_employee_batch(request, db)
    return {"successful_inserts": successful_inserts, "failed_inserts": failed_inserts}

@router.get("/all", response_model=List[HiredEmployeeSchema])
def get_all_hired_employees(db: Session = Depends(get_db)):
    return db_hired_employee.get_all_hired_employees(db)
