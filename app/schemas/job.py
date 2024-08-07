"""Model for Job"""

from pydantic import BaseModel

class JobSchema(BaseModel):
    id: int
    job: str

    class Config:
        orm_mode = True
