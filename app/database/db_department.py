"""File that encapsulates the ORM operations for the Department model"""

from sqlalchemy.orm.session import Session
from database.database_models import SQLDepartment
from schemas.department import DepartmentSchema


def create_department(department: DepartmentSchema, db: Session):
    """ Function that creates a department in the database """
    department = SQLDepartment(**department.dict())
    db.add(department)
    db.commit()
    db.refresh(department)
    return department