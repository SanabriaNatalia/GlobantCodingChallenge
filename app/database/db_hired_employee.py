""" File that encapsulates the ORM operations for the HiredEmployee model """

from sqlalchemy.orm.session import Session
from database.database_models import SQLHiredEmployee
from schemas.hired_employee import HiredEmployeeSchema
from typing import List
import logging


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_hired_employee(hired_employee: HiredEmployeeSchema, db: Session):
    """ Function that creates a hired employee in the database """
    hired_employee = SQLHiredEmployee(**hired_employee.dict())
    db.add(hired_employee)
    db.commit()
    db.refresh(hired_employee)
    return hired_employee

def create_hired_employee_batch(hired_employees: List[HiredEmployeeSchema], db: Session):
    """ Function that creates a batch of hired employees in the database """
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
    
def get_all_hired_employees(db: Session):
    """ Function that retrieves all hired employees from the database """
    return db.query(SQLHiredEmployee).all()
    