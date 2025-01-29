from pydantic import BaseModel, Json
from typing import Optional

class MilestoneEdit(BaseModel):
    name: str
    status: str

class Milestone(MilestoneEdit):
    id: int
    sow_id: int