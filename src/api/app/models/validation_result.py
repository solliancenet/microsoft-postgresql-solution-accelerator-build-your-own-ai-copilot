from pydantic import BaseModel, Json, Field
from typing import List, Optional
from datetime import date, datetime

class ValidationResultBase(BaseModel):
    id: int
    datestamp: datetime
    result: str
    validation_passed: bool

class InvoiceValidationResult(ValidationResultBase):
    invoice_id: int

class SowValidationResult(ValidationResultBase):
    sow_id: int

