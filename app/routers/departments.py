from fastapi import APIRouter, Depends, HTTPException, status
from schemas.department import DepartmentSchema
from database import db_department
from sqlalchemy.orm import Session
from database.database_config import get_db

router = APIRouter(
    prefix="/departments",
    tags=["departments"],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
def create_department(request : DepartmentSchema, db: Session = Depends(get_db)):
    return db_department.create_department(request, db)