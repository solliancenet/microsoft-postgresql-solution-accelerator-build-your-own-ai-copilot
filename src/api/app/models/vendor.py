from pydantic import BaseModel, Json
from typing import Optional

class Vendor(BaseModel):
    id: int
    name: str
    address: str
    contact_name: str
    contact_email: str
    contact_phone: str
    type: str
    metadata: Optional[Json[dict]] = None
