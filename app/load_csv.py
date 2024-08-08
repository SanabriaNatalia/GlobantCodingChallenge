from pyspark.sql import SparkSession
from pyspark.sql.functions import col, to_timestamp, date_format
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from database.database_models import SQLHiredEmployee, SQLDepartment, SQLJob
from database.database_config import SessionLocal, Base, get_db
from schemas.hired_employee import HiredEmployeeSchema
from schemas.department import DepartmentSchema
from schemas.job import JobSchema
import os
import logging
from pydantic import ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Dictionary to map entities to their models, CSV files, and schemas
ENTITY_MAPPING = {
    "departments": {
        "model": SQLDepartment,
        "file_path": "app/data/departments.csv",
        "schema": DepartmentSchema,
        "columns": ["id", "department"]
    },
    "jobs": {
        "model": SQLJob,
        "file_path": "app/data/jobs.csv",
        "schema": JobSchema,
        "columns": ["id", "job"]
    },
    "hired_employees": {
        "model": SQLHiredEmployee,
        "file_path": "app/data/hired_employees.csv",
        "schema": HiredEmployeeSchema,
        "columns": ["id", "name", "datetime", "department_id", "job_id"],
        "timestamp_columns": ["datetime"]
    }
}

def read_and_validate_csv(spark, entity_info):
    """Read and validate CSV file using Spark and Pydantic."""
    # Read the CSV file without headers and assign column names manually
    df = spark.read.csv(entity_info["file_path"], header=False, inferSchema=True)
    df = df.toDF(*entity_info["columns"])
    
    # Convert timestamp columns if specified
    if "timestamp_columns" in entity_info:
        for column in entity_info["timestamp_columns"]:
            if column in df.columns:
                df = df.withColumn(column, to_timestamp(col(column), "yyyy-MM-dd'T'HH:mm:ss'Z'"))
                df = df.withColumn(column, date_format(col(column), "yyyy-MM-dd'T'HH:mm:ss'Z'"))
            else:
                raise ValueError(f"Column {column} not found in {entity_info['file_path']}")

    validated_records = []
    for row in df.toLocalIterator():
        record = row.asDict()
        try:
            validated_record = entity_info["schema"](**record)
            validated_records.append(validated_record.dict())
        except ValidationError as e:
            logger.error(f"Validation error for record {record}: {e}")
            continue

    return validated_records

def insert_ignore_duplicates(session: Session, records, model):
    """Insert validated CSV data into the database, ignoring duplicates."""
    for record in records:
        existing_record = session.query(model).filter_by(id=record['id']).first()
        if not existing_record:
            new_record = model(**record)
            session.add(new_record)
    session.commit()

def load_data():
    """Main function to read CSV files and load data into the database."""
    # Create Spark session
    spark = SparkSession.builder \
        .appName("LoadCSV") \
        .getOrCreate()

    session = next(get_db())
    try:
        for entity, entity_info in ENTITY_MAPPING.items():
            logger.info(f"Processing {entity}")
            validated_records = read_and_validate_csv(spark, entity_info)
            insert_ignore_duplicates(session, validated_records, entity_info["model"])
            logger.info(f"Successfully loaded {entity} from {entity_info['file_path']} into the database")
    except Exception as e:
        logger.error(f"Error loading data into the database: {e}")
        session.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        session.close()
        spark.stop()
    
    return {"status": "success", "message": "All data loaded successfully"}

if __name__ == "__main__":
    load_data()
