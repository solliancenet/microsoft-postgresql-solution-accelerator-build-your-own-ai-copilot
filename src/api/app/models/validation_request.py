from pydantic import BaseModel

class ValidationRequest(BaseModel):
    """Request model for generating a validation."""
    message: str