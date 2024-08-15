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

    serialized_results = [
        {
            "department": result[0],
            "job": result[1],
            "quarter": result[2],
            "employee_count": result[3]
        }
        for result in results
    ]

    return serialized_results

def get_departments_above_average(db: Session):
    
    timestamp_column = func.to_timestamp(SQLHiredEmployee.datetime, 'YYYY-MM-DD"T"HH24:MI:SS"Z"')

    # Subquery to calculate average employees hired in 2021

    dept_counts = db.query(
        SQLDepartment.id,
        func.count(SQLHiredEmployee.id).label('employee_count')
    ).filter(
        func.extract('year', timestamp_column) == 2021
    ).join(
        SQLDepartment, SQLDepartment.id == SQLHiredEmployee.department_id
    ).group_by(
        SQLDepartment.id
    ).subquery()

    avg_hired = db.query(
        func.avg(dept_counts.c.employee_count)
    ).scalar()

    results = db.query(
        SQLDepartment.id,
        SQLDepartment.department,
        dept_counts.c.employee_count
    ).join(
        dept_counts, SQLDepartment.id == dept_counts.c.id
    ).group_by(
        SQLDepartment.id, SQLDepartment.department, dept_counts.c.employee_count
    ).having(
        dept_counts.c.employee_count > avg_hired
    ).order_by(
        dept_counts.c.employee_count.desc()
    ).all()
    
    serialized_results = [
        {"id": dept.id, 
        "department": dept.department, 
        "employee_count": dept.employee_count}
        for dept in results
    ]

    return serialized_results