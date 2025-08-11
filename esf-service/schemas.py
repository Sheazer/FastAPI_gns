from pydantic import BaseModel
from typing import Any
from datetime import datetime

class ESFCreate(BaseModel):
    document_uuid: str | None = None
    legal_person_tin: str
    data: dict

class ESFOut(BaseModel):
    id: int
    document_uuid: str
    legal_person_tin: str
    data: dict
    status: str
    created_by: int | None
    created_at: datetime

    class Config:
        orm_mode = True
