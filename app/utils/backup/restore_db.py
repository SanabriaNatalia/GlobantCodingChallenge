import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from fastavro import reader
from azure.storage.blob import BlobServiceClient
from io import BytesIO
from dotenv import load_dotenv
from database.database_models import SQLHiredEmployee, SQLDepartment, SQLJob
from utils.backup.table_mapping import table_mapping

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

def restore_table(table_model, blob_name):
    """Restore table from an AVRO file in Azure Blob Storage."""
    blob_client = container_client.get_blob_client(blob_name)
    
    # Download the AVRO file to memory using Bytes
    with BytesIO() as buffer:
        blob_client.download_blob().readinto(buffer)
        buffer.seek(0)  # Move to the beginning of the buffer
        
        # Read the AVRO and restore the records
        avro_reader = reader(buffer)
        for record in avro_reader:
            existing_record = session.query(table_model).filter_by(id=record['id']).first()
            if not existing_record:
                new_record = table_model(**record)
                session.add(new_record)
        session.commit()
        
    print(f"Restoration of {table_model.__tablename__} from {blob_name} completed.")

