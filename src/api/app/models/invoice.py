from pydantic import BaseModel, Json, Field
from typing import List, Optional
from datetime import date

class Invoice(BaseModel):
    id: int
    invoice_number: str
    amount: float
    invoice_date: date
    payment_status: str
    document: Optional[str] = None
    invoice_details: Optional[Json[dict]] = None
