"""Model for Department"""

from pydantic import BaseModel

class Department(BaseModel):
    id: int
    department: str
