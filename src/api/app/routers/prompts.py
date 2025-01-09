from app.lifespan_manager import get_db_connection_pool, get_blob_service_client, get_app_config
from app.models import Prompt
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Response, Form
from azure.storage.blob import ContentSettings
from pydantic import parse_obj_as

# Initialize the router
router = APIRouter(
    prefix = "/prompts",
    tags = ["Prompts"],
    dependencies = [Depends(get_db_connection_pool)],
    responses = {404: {"description": "Not found"}}
)

@router.get("/", response_model=list[Prompt])
async def list_prompts(pool = Depends(get_db_connection_pool)):
    """Retrieves a list of prompts from the database."""
    async with pool as conn:
        rows = await conn.fetch('SELECT * FROM prompts ORDER BY name')
        prompts = parse_obj_as(list[Prompt], [dict(row) for row in rows])
    return prompts

@router.get("/{prompt_id}", response_model=Prompt)
async def get_by_id(prompt_id: str, pool = Depends(get_db_connection_pool)):
    """Retrieves a prompt by ID from the database."""
    async with pool as conn:
        row = await conn.fetchrow('SELECT * FROM prompts WHERE id = $1;', prompt_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'A prompt with an id of {prompt_id} was not found.')
        prompt = parse_obj_as(Prompt, dict(row))
    return prompt

@router.put("/", response_model=list[Prompt])
async def update_all_prompts(
    prompts: list[Prompt],
    pool = Depends(get_db_connection_pool)
    ):
    """Updates all prompts in the database."""
    async with pool as conn:
        for prompt in prompts:
            await conn.execute('UPDATE prompts SET prompt = $1 WHERE id = $2;', prompt.prompt, prompt.id)
        rows = await conn.fetch('SELECT * FROM prompts ORDER BY name')
        prompts = parse_obj_as(list[Prompt], [dict(row) for row in rows])
    return prompts
