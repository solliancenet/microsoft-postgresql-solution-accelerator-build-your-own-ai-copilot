from pydantic import BaseModel, Json
from typing import Optional
from datetime import date

class SowEdit(BaseModel):
    number: str
    vendor_id: int
    start_date: date
    end_date: date
    budget: float

class Sow(SowEdit):
    id: int
    document: str
    metadata: Optional[Json[dict]] = None
    


