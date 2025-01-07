from pydantic import BaseModel, Json, Field
from typing import List, Optional
from datetime import date

class InvoiceEdit(BaseModel):
    number: str
    amount: float
    invoice_date: date
    payment_status: str
    document: Optional[str] = None
    metadata: Optional[Json[dict]] = None

class Invoice(InvoiceEdit):
    id: int
