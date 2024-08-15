""" File that encapsulates de analytics needed for the application in the Challenge 2 """

from sqlalchemy.orm.session import Session
from sqlalchemy import func, case
from database.database_models import SQLHiredEmployee, SQLDepartment, SQLJob

def get_employees_per_quarter(db: Session):
    """ Query to get the number of employees hired per quarter in 2021 """
    
    timestamp_column = func.to_timestamp(SQLHiredEmployee.datetime, 'YYYY-MM-DD"T"HH24:MI:SS"Z"')

    quarter_case = case(
        (func.extract('month', timestamp_column).between(1, 3), 1),
        (func.extract('month', timestamp_column).between(4, 6), 2),
        (func.extract('month', timestamp_column).between(7, 9), 3),
        (func.extract('month', timestamp_column).between(10, 12), 4),
    ).label('quarter')

    results = db.query(
        SQLDepartment.department,
        SQLJob.job,
        quarter_case,
        func.count(SQLHiredEmployee.id).label('employee_count')
    ).join(SQLDepartment, SQLDepartment.id == SQLHiredEmployee.department_id
    ).join(SQLJob, SQLJob.id == SQLHiredEmployee.job_id
    ).filter(
        func.extract('year', timestamp_column) == 2021
    ).group_by(
        SQLDepartment.department, SQLJob.job, quarter_case
    ).order_by(
        SQLDepartment.department, SQLJob.job
    ).all()

    results_dict = [
        {
            "department": result[0],
            "job": result[1],
            "quarter": result[2],
            "employee_count": result[3]
        }
        for result in results
    ]

    return results_dict

def get_departments_above_average(db: Session):
    # Subconsulta para calcular la media
    avg_hired = db.query(
        func.avg(func.count(SQLHiredEmployee.id))
    ).join(
        SQLDepartment, SQLDepartment.id == SQLHiredEmployee.department_id
    ).group_by(SQLDepartment.id).scalar()

    # Consulta principal para filtrar departamentos que superan la media
    results = db.query(
        SQLDepartment.id,
        SQLDepartment.department,
        func.count(SQLHiredEmployee.id).label('employee_count')
    ).join(
        SQLDepartment, SQLDepartment.id == SQLHiredEmployee.department_id
    ).group_by(SQLDepartment.id
    ).having(
        func.count(SQLHiredEmployee.id) > avg_hired
    ).order_by(
        func.count(SQLHiredEmployee.id).desc()
    ).all()

    return results