
from app.lifespan_manager import get_embedding_client
from fastapi import APIRouter, Depends

# Initialize the router
router = APIRouter(
    prefix = "",
    tags = ["Embeddings"],
    dependencies = [Depends(get_embedding_client)],
    responses = {404: {"description": "Not found"}}
)

@router.get('/embeddings', response_model = list[float])
async def generate_embeddings(text: str, client = Depends(get_embedding_client)):
    """Generate embeddings for the provided text using Azure OpenAI."""
    return await client.aembed_query(text)
