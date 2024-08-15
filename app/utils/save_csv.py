import pandas as pd
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from io import BytesIO
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to the Data Lake
storage_connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
container_name = 'globant-challenge'
container_client = blob_service_client.get_container_client(container_name)

# Fuction to read an Excel file from the Data Lake
def read_excel_from_datalake(blob_name, sheet_name):
    blob_client = container_client.get_blob_client(blob_name)
    blob_data = blob_client.download_blob().readall()
    df = pd.read_excel(BytesIO(blob_data), sheet_name=sheet_name)
    return df

# Function to write a DataFrame to a CSV file in the Data Lake
def write_csv_to_datalake(df, blob_name):
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False, sep=',')
    blob_client = container_client.get_blob_client(blob_name)
    blob_client.upload_blob(csv_buffer.getvalue(), blob_type="BlockBlob", overwrite=True)

# Read and write files to the Data Lake

# Departments
df_departments = read_excel_from_datalake('data/excel/departments.xlsx', 'departments')
write_csv_to_datalake(df_departments, 'data/csv/departments.csv')

# Hired employees
df_hired_employees = read_excel_from_datalake('data/excel/hired_employees.xlsx', 'hired_employees')
write_csv_to_datalake(df_hired_employees, 'data/csv/hired_employees.csv')

# Jobs
df_jobs = read_excel_from_datalake('data/excel/jobs.xlsx', 'jobs')
write_csv_to_datalake(df_jobs, 'data/csv/jobs.csv')