from pydantic import BaseModel
from typing import List, Optional
from datetime import date

class InvoiceBase(BaseModel):
    invoice_number: str
    amount: Optional[float] = None
    invoice_date: Optional[date] = None
    payment_status: Optional[str] = None
    invoice_details: Optional[dict] = None

class InvoiceCreate(InvoiceBase):
    pass

class Invoice(InvoiceBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
