from pydantic import BaseModel

class Vendor(BaseModel):
    id: int
    name: str
    contact_name: str
    contact_email: str
    contact_phone: str
    address: str
    type: str
