from pydantic import BaseModel, Json
from typing import Optional
from datetime import date

class MsaEdit(BaseModel):
    vendor_id: int
    title: str
    start_date: date
    end_date: Optional[date] = None
    metadata: Optional[Json[dict]] = None
    document: Optional[str] = None

class Msa(MsaEdit):
    id: int   

