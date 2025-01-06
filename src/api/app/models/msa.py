from pydantic import BaseModel, Json
from typing import Optional
from datetime import date

class MsaEdit(BaseModel):
    msa_title: str
    start_date: date
    end_date: Optional[date] = None
    additional_info: Optional[Json[dict]] = None

class Msa(MsaEdit):
    id: int
    msa_document: str
    

