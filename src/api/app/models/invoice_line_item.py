from pydantic import BaseModel, Json, Field
from typing import List, Optional
from datetime import date

class InvoiceLineItemEdit(BaseModel):
    invoice_id: int
    description: str
    amount: float
    status: str
    due_date: date

class InvoiceLineItem(InvoiceLineItemEdit):
    id: int
