from pydantic import BaseModel, Json
from typing import Optional

class Prompt(BaseModel):
    id: str
    name: str
    prompt: Optional[str] = None
