from pydantic import BaseModel, Json
from typing import Optional
from datetime import date

class Sow(BaseModel):
    id: int
    title: str
    start_date: date
    end_date: date
    budget: float
    document: str
    details: Optional[Json[dict]] = None

class SowEdit(BaseModel):
    sow_title: str
    start_date: date
    end_date: date
    budget: float
