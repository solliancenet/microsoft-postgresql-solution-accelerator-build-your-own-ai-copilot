from pydantic import BaseModel
from typing import Optional

class Company(BaseModel):
    id: int
    company_name: str
    address: Optional[str] = None
    contact_person: Optional[str] = None
    contact_email: Optional[str] = None
    extra_metadata: Optional[dict] = None
