from database.database_models import SQLHiredEmployee, SQLDepartment, SQLJob
from schemas.hired_employee import HiredEmployeeSchema
from schemas.department import DepartmentSchema
from schemas.job import JobSchema

def pydantic_to_avro_schema(pydantic_model, name):
    """Convert Pydantic model to AVRO schema."""
    fields = []
    for field_name, field_type in pydantic_model.__annotations__.items():
        avro_type = 'string'  # Default to string for simplicity
        if field_type == int:
            avro_type = 'int'
        elif field_type == float:
            avro_type = 'float'
        elif field_type == bool:
            avro_type = 'boolean'
        fields.append({"name": field_name, "type": avro_type})
    return {
        "type": "record",
        "name": name,
        "fields": fields
    }

table_mapping = {
    "departments": {
        "model": SQLDepartment,
        "schema": pydantic_to_avro_schema(DepartmentSchema, "Department"),
        "blob_name": "backups/departments.avro"
    },
    "jobs": {
        "model": SQLJob,
        "schema": pydantic_to_avro_schema(JobSchema, "Job"),
        "blob_name": "backups/jobs.avro"
    },
    "hired_employees": {
        "model": SQLHiredEmployee,
        "schema": pydantic_to_avro_schema(HiredEmployeeSchema, "HiredEmployee"),
        "blob_name": "backups/hired_employees.avro"
    }
}

