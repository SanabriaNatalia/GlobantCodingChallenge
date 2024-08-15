""" File that encapsulates the ORM operations for the HiredEmployee model """

from sqlalchemy.orm.session import Session
from database.database_models import SQLHiredEmployee, SQLDepartment, SQLJob
from schemas.hired_employee import HiredEmployeeSchema
from typing import List
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_hired_employee(hired_employee: HiredEmployeeSchema, db: Session):
    """ Function that creates a hired employee in the database """

    # Verify existence of department_id
    if not db.query(SQLDepartment).filter(SQLDepartment.id == hired_employee.department_id).first():
        raise ValueError(f"Department ID {hired_employee.department_id} does not exist")
    
    # Verify existence of job_id
    if not db.query(SQLJob).filter(SQLJob.id == hired_employee.job_id).first():
        raise ValueError(f"Job ID {hired_employee.job_id} does not exist")

    hired_employee = SQLHiredEmployee(**hired_employee.dict())
    db.add(hired_employee)
    db.commit()
    db.refresh(hired_employee)
    return hired_employee

def create_hired_employee_batch(hired_employees: List[HiredEmployeeSchema], db: Session):
    """ Function that creates a batch of hired employees in the database """

    successful_inserts = []
    failed_inserts = []

    for employee in hired_employees:
        try:
            # Verify existence of department_id
            if not db.query(SQLDepartment).filter(SQLDepartment.id == hired_employee.department_id).first():
                raise ValueError(f"Department ID {hired_employee.department_id} does not exist")
            
            # Verify existence of job_id
            if not db.query(SQLJob).filter(SQLJob.id == hired_employee.job_id).first():
                raise ValueError(f"Job ID {hired_employee.job_id} does not exist")

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
    
def get_all_hired_employees(db: Session):
    """ Function that retrieves all hired employees from the database """
    return db.query(SQLHiredEmployee).all()

def get_hired_employee_by_id(hired_employee_id: int, db: Session):
    """ Function that retrieves a hired employee by its ID """
    return db.query(SQLHiredEmployee).filter(SQLHiredEmployee.id == hired_employee_id).first()

def update_hired_employee(hired_employee_id: int, hired_employee: HiredEmployeeSchema, db: Session):
    """ Function that updates a hired employee by its ID """
    employee = db.query(SQLHiredEmployee).filter(SQLHiredEmployee.id == hired_employee_id)
    employee.update(**hired_employee.dict())
    db.commit()
    return employee.first()

def delete_hired_employee(hired_employee_id: int, db: Session):
    """ Function that deletes a hired employee by its ID """
    employee = db.query(SQLHiredEmployee).filter(SQLHiredEmployee.id == hired_employee_id)
    employee.delete(synchronize_session=False)
    db.commit()
    return employee.first()
