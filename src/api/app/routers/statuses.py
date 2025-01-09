from app.lifespan_manager import get_db_connection_pool, get_blob_service_client, get_app_config
from app.models import Status
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Response, Form
from azure.storage.blob import ContentSettings
from pydantic import parse_obj_as

# Initialize the router
router = APIRouter(
    prefix = "/statuses",
    tags = ["Statuses"],
    dependencies = [Depends(get_db_connection_pool)],
    responses = {404: {"description": "Not found"}}
)

@router.get("/", response_model=list[Status])
async def list_statuses(pool = Depends(get_db_connection_pool)):
    """Retrieves a list of statuses from the database."""
    async with pool as conn:
        rows = await conn.fetch('SELECT * FROM status ORDER BY name')
        statuses = parse_obj_as(list[Status], [dict(row) for row in rows])
    return statuses