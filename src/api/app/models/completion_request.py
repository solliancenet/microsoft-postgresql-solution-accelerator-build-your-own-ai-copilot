from pydantic import BaseModel

class ChatItem(BaseModel):
    role: str
    content: str

class CompletionRequest(BaseModel):
    """Request model for generating a chat completion."""
    message: str
    chat_history: list[ChatItem]
    max_history: int = 6
