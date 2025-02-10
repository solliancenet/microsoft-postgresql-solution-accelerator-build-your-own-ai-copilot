from pydantic import BaseModel

class CompletionRequest(BaseModel):
    """Request model for generating a chat completion."""
    session_id: int
    message: str
    max_history: int = 6
