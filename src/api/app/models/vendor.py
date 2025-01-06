from pydantic import BaseModel, Json
from typing import Optional

class VendorEdit(BaseModel):
    name: str
    address: str
    contact_name: str
    contact_email: str
    contact_phone: str
    type: str
    metadata: Optional[Json[dict]] = None

class Vendor(VendorEdit):
    id: int


