from pydantic import BaseModel
from typing import List, Optional

class VendorBase(BaseModel):
    name: str
    address: Optional[str] = None
    contact_name: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    contact_type: Optional[str] = None

class VendorCreate(VendorBase):
    pass

class Vendor(VendorBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
