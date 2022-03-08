from pydantic import BaseModel, EmailStr
from typing import Optional


class DataAnswers(BaseModel):
    tel: Optional[int] = None
    email: Optional[EmailStr] = None
    other: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True


class AnswersInDB(BaseModel):
    typ: Optional[str] = "unwatched"
    site_name: str
    data: DataAnswers

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True
