"""File that contains the database models for the application"""

from sqlalchemy import Column, Integer, String
from .database_config import Base

class SQLHiredEmployee(Base):
    __tablename__ = "hired_employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    datetime = Column(String)  # Saved as String
    department_id = Column(Integer)
    job_id = Column(Integer)

class SQLDepartment(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, index=True)

class SQLJob(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job = Column(String, index=True)
