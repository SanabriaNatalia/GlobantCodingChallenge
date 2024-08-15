"""Main module for the FastAPI application"""

from fastapi import FastAPI, HTTPException, Depends
from routers import hired_employees, departments, jobs, backup
from database.database_config import get_db
from sqlalchemy.orm.session import Session

# Initialize App
app = FastAPI()

# Include routers
app.include_router(hired_employees.router)
app.include_router(departments.router)
app.include_router(jobs.router)
app.include_router(backup.router)

@app.get("/")
def hello():
    return {"message": "Hello Globant!"}
