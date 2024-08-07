"""Main module for the FastAPI application"""

from fastapi import FastAPI
from app.models.hired_employee import HiredEmployee
from app.models.department import Department
from app.models.job import Job


# Initialize App
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}