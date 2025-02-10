from pydantic import BaseModel

class CompletionResponse(BaseModel):
    """Response model for generating a chat completion."""
    session_id: int
    content: str
