from app.lifespan_manager import get_db_connection_pool, get_blob_service_client, get_app_config
from app.models import Sow, SowEdit, ListResponse
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Response, Form
from azure.storage.blob import ContentSettings
from datetime import datetime
from pydantic import parse_obj_as

# Initialize the router
router = APIRouter(
    prefix = "/sows",
    tags = ["SOWs"],
    dependencies = [Depends(get_db_connection_pool)],
    responses = {404: {"description": "Not found"}}
)


@router.get("/", response_model=ListResponse[Sow])
async def list_sows(skip: int = 0, limit: int = 10, sortby: str = None, search: str = None, pool = Depends(get_db_connection_pool), blob_service_client = Depends(get_blob_service_client)):
    """Retrieves a list of SOWs from the database."""
    async with pool.acquire() as conn:
        orderby = 'id'
        if (sortby):
            orderby = sortby
        rows = await conn.fetch('SELECT * FROM sows ORDER BY $1 LIMIT $2 OFFSET $3;', orderby, limit, skip)
        sows = parse_obj_as(list[Sow], [dict(row) for row in rows])

        total = await conn.fetchval('SELECT COUNT(*) FROM sows;')

    return ListResponse[Sow](data=sows, total = total, skip = skip, limit = limit)

@router.get("/{sow_id}", response_model=Sow)
async def get_by_id(sow_id: int, pool = Depends(get_db_connection_pool)):
    """Retrieves a SOW by ID from the database."""
    async with pool.acquire() as conn:
        row = await conn.fetchrow('SELECT * FROM sows WHERE id = $1;', sow_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'A SOW with an id of {sow_id} was not found.')
        sow = parse_obj_as(Sow, dict(row))
    return sow

@router.post("/", response_model=Sow)
async def create_sow(
    number: str = Form(...),
    msa_id: int = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    budget: float = Form(...),
    file: UploadFile = File(...),
    pool = Depends(get_db_connection_pool),
    appConfig = Depends(get_app_config),
    blob_service_client = Depends(get_blob_service_client)
):
    # Parse dates
    start_date_parsed = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_parsed = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Parse budget
    budget_parsed = float(budget)

    # Upload file to Azure Blob Storage
    container_name = appConfig.get_document_container_name()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)

    content_settings = ContentSettings(
        content_type=file.content_type,
        content_disposition=f'attachment; filename="{file.filename}"'
    )

    blob_client.upload_blob(file.file, overwrite=True, content_settings=content_settings)

    # # Create SOW in the database
    async with pool.acquire() as conn:
        sow = await conn.fetchrow('''
            INSERT INTO sows (number, start_date, end_date, budget, document, metadata, msa_id, msa_title)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
            RETURNING *;
        ''', number, start_date_parsed, end_date_parsed, budget_parsed, file.filename, '{}', msa_id, 'N/A')
        
        sow = parse_obj_as(Sow, dict(sow))
    return sow

@router.put("/{sow_id}", response_model=Sow)
async def update_sow(sow_id: int, sow_update: SowEdit, pool = Depends(get_db_connection_pool)):
    """Updates a SOW in the database."""
    async with pool.acquire() as conn:
        sow = await get_by_id(sow_id, pool)
        if sow is None:
            raise HTTPException(status_code=404, detail=f'A SOW with an id of {sow_id} was not found.')

        sow.number = sow_update.number
        sow.start_date = sow_update.start_date
        sow.end_date = sow_update.end_date
        sow.budget = sow_update.budget
        sow.msa_id = sow_update.msa_id

        # for key, value in sow_update.dict().items():
        #     setattr(sow, key, value)
        row = await conn.fetchrow('''
            UPDATE sows
            SET number = $1, start_date = $2, end_date = $3, budget = $4, msa_id = $5
            WHERE id = $6
            RETURNING *;''',
            sow.number, sow.start_date, sow.end_date, sow.budget, sow.msa_id, sow_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'A SOW with an id of {sow_id} was not found.')
        updated_sow = parse_obj_as(Sow, dict(row))
    return updated_sow

@router.delete("/{id}", response_model=Sow)
async def delete_sow(id: int, pool = Depends(get_db_connection_pool)):
    """Deletes a SOW from the database."""   
    async with pool.acquire() as conn:
        row = await conn.fetchrow('DELETE FROM sows WHERE id = $1 RETURNING *;', id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'A SOW with an id of {id} was not found.')
        deleted_sow = parse_obj_as(Sow, dict(row))
    return deleted_sow