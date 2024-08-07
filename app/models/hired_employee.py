"""Model for HiredEmployee"""

from pydantic import BaseModel, Field, validator
from datetime import datetime


class HiredEmployee(BaseModel):
    id: int
    name: str
    datetime: str
    department_id: int
    job_id: int

    @validator('datetime')
    def check_datetime_format(cls, v):
        try:
            # Verificar si el string está en el formato ISO
            datetime.fromisoformat(v.replace("Z", "+00:00"))
        except ValueError:
            raise ValueError("datetime must be in ISO format")
        return v
    
    class Config:
        orm_mode = True