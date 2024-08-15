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

# Configure Azure Blob Storage
connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = "globant-challenge"
container_client = blob_service_client.get_container_client(container_name)

def restore_table_from_backup(table_name, session: Session):
    """Restore a table from an AVRO file in Azure Blob Storage."""
    if table_name not in table_mapping:
        raise ValueError(f"Table {table_name} not found.")

    table_info = table_mapping[table_name]
    model = table_info["model"]
    blob_name = table_info["blob_name"]

    blob_client = container_client.get_blob_client(blob_name)

    # Verify the existence of the backup file
    if not blob_client.exists():
        raise ValueError(f"Backup file {blob_name} not found in Azure Blob Storage.")
    
    # Verify that the backup file is not empty or corrupted
    try:
        with BytesIO() as buffer:
            blob_client.download_blob().readinto(buffer)
            buffer.seek(0)  

            # try to read the backup file
            avro_reader = reader(buffer)
            records = [record for record in avro_reader]
            
            if not records:
                raise ValueError("Backup file is empty or corrupted.")
    except Exception as e:
        raise ValueError(f"Failed to read backup file {blob_name}: {str(e)}")

    # Delete all existing records from the table
    session.query(model).delete()
    session.commit()

    # Restore the records from the backup file
    for record in records:
        new_record = model(**record)
        session.add(new_record)
    session.commit()
        
    return f"Restoration of {table_name} from {blob_name} completed, replacing all existing data."