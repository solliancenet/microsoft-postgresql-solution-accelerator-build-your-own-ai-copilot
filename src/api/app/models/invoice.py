from pydantic import BaseModel, Json, Field
from typing import List, Optional
from datetime import date

class InvoiceEdit(BaseModel):
    vendor_id: int
    sow_id: int
    number: str
    amount: float
    invoice_date: date
    payment_status: str
    document: Optional[str] = None
    metadata: Optional[Json[dict]] = None

class Invoice(InvoiceEdit):
    id: int
