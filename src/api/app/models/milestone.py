from pydantic import BaseModel, Json
from typing import Optional
from datetime import date

class MilestoneEdit(BaseModel):
    name: str
    status: str
    due_date: Optional[date] = None

class Milestone(MilestoneEdit):
    id: int
    sow_id: int