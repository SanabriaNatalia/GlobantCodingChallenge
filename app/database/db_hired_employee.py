""" File that encapsulates the ORM operations for the HiredEmployee model """

from sqlalchemy.orm.session import Session
from database.database_models import SQLHiredEmployee
from schemas.hired_employee import HiredEmployeeSchema


def create_hired_employee(hired_employee: HiredEmployeeSchema, db: Session):
    """ Function that creates a hired employee in the database """
    hired_employee = SQLHiredEmployee(**hired_employee.dict())
    db.add(hired_employee)
    db.commit()
    db.refresh(hired_employee)
    return hired_employee