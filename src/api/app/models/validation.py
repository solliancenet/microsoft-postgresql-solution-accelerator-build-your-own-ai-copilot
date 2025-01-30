from app.models import Invoice, Sow, Milestone, Deliverable, InvoiceLineItem, Vendor
from pydantic import parse_obj_as, BaseModel
from typing import Optional

class InvoiceModel(Invoice):
    vendor: Optional[Vendor] = None
    line_items: Optional[list[InvoiceLineItem]] = None
    
class SowModel(Sow):
    milestones: Optional[list[Milestone]] = None

class MilestoneModel(Milestone):
    deliverables: Optional[list[Deliverable]] = None