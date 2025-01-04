from pydantic import BaseModel, Json
from typing import Optional
from datetime import date

class Msa(BaseModel):
    id: int
    msa_title: str
    start_date: date
    end_date: Optional[date] = None
    additional_info: Optional[Json[dict]] = None
