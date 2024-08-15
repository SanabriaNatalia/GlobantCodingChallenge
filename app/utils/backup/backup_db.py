import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from fastavro import writer, parse_schema
from azure.storage.blob import BlobServiceClient
from io import BytesIO
from dotenv import load_dotenv
from schemas.hired_employee import HiredEmployeeSchema
from schemas.department import DepartmentSchema
from schemas.job import JobSchema
from database.database_models import SQLHiredEmployee, SQLDepartment, SQLJob
from utils.backup.table_mapping import table_mapping, pydantic_to_avro_schema

# Load environment variables
load_dotenv()

# Configure the database session
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
session = Session(engine)

# Configure Azure Blob Storage
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = "globant-challenge"
container_client = blob_service_client.get_container_client(container_name)

def backup_table(table_name):
    """Backup a table to an AVRO file in Azure Blob Storage."""
    
    if table_name not in table_mapping:
        raise ValueError(f"Table {table_name} not found.")

    table_info = table_mapping[table_name]
    model = table_info["model"]
    schema = table_info["schema"]
    blob_name = table_info["blob_name"]

    parsed_schema = parse_schema(schema)
    records = session.query(model).all()

    # Serialize the records to an AVRO file in memory
    with BytesIO() as buffer:
        writer(buffer, parsed_schema, [record.__dict__ for record in records])
        buffer.seek(0)  # Return to the beginning of the buffer

        # Upload the AVRO file to Azure Blob Storage
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(buffer, overwrite=True)

    return f"Backup of {table_name} completed and uploaded to Azure Blob Storage as {blob_name}"