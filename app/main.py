"""Main module for the FastAPI application"""

from fastapi import FastAPI
from database.database_config import SessionLocal, engine
from database.database_models import SQLHiredEmployee, SQLDepartment, SQLJob
from models.hired_employee import HiredEmployee
from models.department import Department
from models.job import Job


# Initialize App
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}