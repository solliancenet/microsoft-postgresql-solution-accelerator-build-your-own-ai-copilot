from app.lifespan_manager import get_azure_openai_chat_client
from app.models import CompletionRequest
from fastapi import APIRouter, Depends, HTTPException

# Initialize the router
router = APIRouter(
    prefix = "/completions",
    tags = ["Completions"],
    dependencies = [Depends(get_azure_openai_chat_client)],
    responses = {404: {"description": "Not found"}}
)

@router.post('/chat', response_model = str)
async def generate_chat_completion(request: CompletionRequest, client = Depends(get_azure_openai_chat_client)):
    """Generate a chat completion using the Azure OpenAI API."""
    # TODO: Get the Azure OpenAI API deployment names from app settings    
    COMPLETION_DEPLOYMENT_NAME = "completions"

    # Define the system prompt that contains the assistant's persona.
    system_prompt = """
    You are an intelligent copilot for Woodgrove designed to help users manage statements of work (SOWs) and invoices.
    You are helpful, friendly, and knowledgeable, but can only answer questions about Woodgrove's contracts and associated invoices.
    You are not able to provide legal advice or financial information.
    """
    # Provide the copilot with a persona using the system prompt.
    messages = [{ "role": "system", "content": system_prompt }]

    # Add the chat history to the messages list
    for message in request.chat_history[-request.max_history:]:
        messages.append(message)

    # Add the current user message to the messages list
    messages.append({"role": "user", "content": request.message})

    # Create Azure OpenAI client
    async with client:
        response = await client.embeddings.create(
            input = text,
            model = EMBEDDING_DEPLOYMENT_NAME
        )
        return response.data[0].embedding