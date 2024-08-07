"""Main module for the FastAPI application"""

from fastapi import FastAPI
from routers import hired_employees, departments, jobs

# Initialize App
app = FastAPI()

# Include routers
app.include_router(hired_employees.router)
app.include_router(departments.router)
app.include_router(jobs.router)

@app.get("/hello")
def hello():
    return {"message": "Hello World!"}