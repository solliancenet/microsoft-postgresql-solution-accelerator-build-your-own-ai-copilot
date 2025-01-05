from pydantic import BaseModel, Json
from typing import Optional
from datetime import date

class SowEdit(BaseModel):
    sow_title: str
    start_date: date
    end_date: date
    budget: float

class Sow(SowEdit):
    id: int
    document: str
    details: Optional[Json[dict]] = None
    


