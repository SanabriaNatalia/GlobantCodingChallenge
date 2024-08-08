"""File that contains the database models for the application"""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database_config import Base

class SQLHiredEmployee(Base):
    __tablename__ = "hired_employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    datetime = Column(String)  # Saved as String
    department_id = Column(Integer, ForeignKey("departments.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))

    # Define relationships
    department = relationship("SQLDepartment", back_populates="employees")
    job = relationship("SQLJob", back_populates="employees")

class SQLDepartment(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    department = Column(String, index=True)

    # Define inverse relationship
    employees = relationship("SQLHiredEmployee", back_populates="department")

class SQLJob(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    job = Column(String, index=True)

    # Define inverse relationship
    employees = relationship("SQLHiredEmployee", back_populates="job")
