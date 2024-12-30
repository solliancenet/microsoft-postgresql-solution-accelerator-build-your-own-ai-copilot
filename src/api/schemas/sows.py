from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class SowBase(BaseModel):
    sow_title: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = None
    sow_document: Optional[str] = None
    details: Optional[dict] = None

class SowEdit(SowBase):
    pass

class Sow(SowBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
