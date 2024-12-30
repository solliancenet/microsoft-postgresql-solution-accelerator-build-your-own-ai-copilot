from pydantic import BaseModel

class CompletionRequest(BaseModel):
    """Request model for generating a chat completion."""
    message: str
    chat_history: list[str]
    max_history: int = 6