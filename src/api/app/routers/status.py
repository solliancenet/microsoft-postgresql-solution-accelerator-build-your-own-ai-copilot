"""
Status API endpoint that acts as a health check for the API.
"""
from fastapi import APIRouter

router = APIRouter(
    prefix = "",
    tags = ["Status"]
)

@router.get("/status")
async def get():
    """Health probe endpoint for the API."""
    return {"status": "ready"}