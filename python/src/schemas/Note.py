from pydantic import BaseModel, Field
from datetime import datetime


class Note(BaseModel):
    # id: str = Field(..., alias="_id")
    title: str = Field(...)
    content: str = Field(...)
    createdAt: datetime = Field(...)
    updatedAt: datetime = Field(...)

    class Config:
        validate_by_name = True
        arbitrary_types_allowed = True
        extra = "allow"
