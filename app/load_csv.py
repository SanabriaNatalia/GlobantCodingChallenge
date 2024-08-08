""" File that loads the CSV file into the database """

import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from app.database.database_models import SQLHiredEmployee, SQLDepartment, SQLJob
from app.database.database_config import Base
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def load_csv_to_db(session: Session, file_path: str, model):
    data = pd.read_csv(file_path)
    data = data.to_dict(orient='records')
    records = [model(**record) for record in data]
    session.bulk_save_objects(records)
    session.commit()

def main():
    Base.metadata.create_all(bind=engine)
    session = Session(bind=engine)

    # Cargar datos de departments.csv
    load_csv_to_db(session, 'app/csv_data/departments.csv', SQLDepartment)

    # Cargar datos de jobs.csv
    load_csv_to_db(session, 'app/csv_data/jobs.csv', SQLJob)

    # Cargar datos de hired_employees.csv
    load_csv_to_db(session, 'app/csv_data/hired_employees.csv', SQLHiredEmployee)

    session.close()

if __name__ == "__main__":
    main()