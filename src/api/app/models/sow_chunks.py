from pydantic import BaseModel, Json
from typing import Optional
from datetime import date

class SowChunk(BaseModel):
    sow_id: int
    heading: str
    content: str
    page_number: int
    