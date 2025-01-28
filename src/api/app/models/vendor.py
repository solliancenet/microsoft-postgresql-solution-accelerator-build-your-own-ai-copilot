from pydantic import BaseModel, Json
from typing import Optional

class VendorEdit(BaseModel):
    name: str
    address: str
    contact_name: str
    contact_email: str
    contact_phone: str
    website: Optional[str] = None
    type: str

class Vendor(VendorEdit):
    id: int


