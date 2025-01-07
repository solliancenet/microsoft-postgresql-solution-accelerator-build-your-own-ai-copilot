from pydantic import BaseModel, Json
from typing import Optional
from datetime import date

class DeliverableEdit(BaseModel):
    milestone_id: int
    deliverable_name: str
    description: str
    amount: Optional[float]
    deliverable_status: str

class Deliverable(DeliverableEdit):
    id: int
