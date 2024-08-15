"""This module contains the backup and restore endpoints for the API."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasicCredentials
from database.db_analytics import get_employees_per_quarter, get_departments_above_average
from security.auth import authenticate
from sqlalchemy.orm import Session
from database.database_config import get_db

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"],
    responses={404: {"description": "Not found"}},
)

@router.get("/employees-per-quarter")
def employees_per_quarter(db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(authenticate)):
    results = get_employees_per_quarter(db)
    return {"data": results}

@router.get("/departments-above-average")
def departments_above_average(db: Session = Depends(get_db), credentials: HTTPBasicCredentials = Depends(authenticate)):
    results = get_departments_above_average(db)
    return {"data": results}