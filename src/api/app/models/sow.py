from pydantic import BaseModel
from typing import Optional
from datetime import date

class Sow(BaseModel):
    id: int
    sow_title: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = None
    sow_document: Optional[str] = None
    details: Optional[dict] = None

class SowEdit(BaseModel):
    sow_title: str
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    budget: Optional[float] = None
