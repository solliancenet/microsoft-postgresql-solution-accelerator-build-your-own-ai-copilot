from pydantic import BaseModel, Json
from typing import Optional
from datetime import date

class DeliverableEdit(BaseModel):
    description: str
    amount: Optional[float]
    status: str
    due_date: date

class Deliverable(DeliverableEdit):
    id: int
    milestone_id: int
