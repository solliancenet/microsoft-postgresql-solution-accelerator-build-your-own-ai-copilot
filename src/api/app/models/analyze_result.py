from pydantic import BaseModel, Json, Field
from typing import List, Optional
from datetime import date, datetime
from .invoice import Invoice
from .sow import Sow

class AnalyzeResultBase(BaseModel):
    hasError: bool = False
    error: Optional[str] = None
    message: Optional[str] = None

class InvoiceAnalyzeResult(AnalyzeResultBase):
    invoice: object = None 

class SowAnalyzeResult(AnalyzeResultBase):
    sow: object = None
