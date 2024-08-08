"""File that encapsulates the ORM operations for the Department model"""

from sqlalchemy.orm.session import Session
from database.database_models import SQLDepartment
from schemas.department import DepartmentSchema
from typing import List
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_department(department: DepartmentSchema, db: Session):
    """ Function that creates a department in the database """
    department = SQLDepartment(**department.dict())
    db.add(department)
    db.commit()
    db.refresh(department)
    return department

def create_department_batch(departments: List[DepartmentSchema], db: Session):
    """ Function that creates a list of departments in the database """

    if not (1 <= len(hired_employees) <= 1000):
        raise ValueError("Batch size must be between 1 and 1000")

    successful_inserts = []
    failed_inserts = []

    for employee in hired_employees:
        try:
            db_hired_employee = SQLHiredEmployee(**employee.dict())
            db.add(db_hired_employee)
            db.commit()
            db.refresh(db_hired_employee)
            successful_inserts.append(db_hired_employee)
            logger.info(f"Successfully inserted: {employee.dict()}")
        except Exception as e:
            db.rollback()
            failed_inserts.append({"record": employee.dict(), "error": str(e)})
            logger.error(f"Failed to insert: {employee.dict()} with error: {str(e)}")
    
    return successful_inserts, failed_inserts

def get_all_departments(db: Session):
    """ Function that retrieves all departments from the database """
    return db.query(SQLDepartment).all()

def get_department_by_id(department_id: int, db: Session):
    """ Function that retrieves a department by its ID """
    return db.query(SQLDepartment).filter(SQLDepartment.id == department_id).first()
    