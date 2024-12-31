from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class Invoice(BaseModel):
    id: int
    invoice_number: str
    amount: Optional[float] = None
    invoice_date: Optional[date] = None
    payment_status: Optional[str] = None
    invoice_details: Optional[dict] = None
