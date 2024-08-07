from fastapi import APIRouter, Depends
from schemas.hired_employee import HiredEmployeeSchema
from database import db_hired_employee
from sqlalchemy.orm.session import Session
from database.database_config import get_db

router = APIRouter(
    prefix="/hired_employees",
    tags=["hired_employees"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def create_hired_employee(request : HiredEmployeeSchema, db: Session = Depends(get_db)):
    return db_hired_employee.create_hired_employee(request, db)