"""Model for Department"""

from pydantic import BaseModel

class DepartmentSchema(BaseModel):
    id: int
    department: str

    class Config:
        orm_mode = True
