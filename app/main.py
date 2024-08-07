"""Main module for the FastAPI application"""

from fastapi import FastAPI

# Initialize App
app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}