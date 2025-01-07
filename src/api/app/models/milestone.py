from pydantic import BaseModel, Json
from typing import Optional
from datetime import date

class MilestoneEdit(BaseModel):
    sow_id: int
    milestone_name: str
    milestone_status: str
    due_date: Optional[date] = None

class Milestone(MilestoneEdit):
    id: int