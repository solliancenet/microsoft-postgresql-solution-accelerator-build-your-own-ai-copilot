from app.lifespan_manager import get_db_connection_pool, get_blob_service_client, get_app_config
from app.models import Msa, MsaEdit, ListResponse
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Response, Form
from azure.storage.blob import ContentSettings
from pydantic import parse_obj_as
from datetime import datetime

# Initialize the router
router = APIRouter(
    prefix = "/msas",
    tags = ["MSAs"],
    dependencies = [Depends(get_db_connection_pool)],
    responses = {404: {"description": "Not found"}}
)

@router.get("/", response_model=ListResponse[Msa])
async def list_msas(skip: int = 0, limit: int = 10, sortby: str = None, search: str = None, pool = Depends(get_db_connection_pool)):
    """Retrieves a list of msas from the database."""
    async with pool.acquire() as conn:
        orderby = 'id'
        if (sortby):
            orderby = sortby
        print (f'orderby: {orderby}')
        
        if (limit >= 0):
            rows = await conn.fetch('SELECT * FROM msas ORDER BY $1 LIMIT $2 OFFSET $3;', orderby, limit, skip)
        else: # If Limit == -1 then No Limit
            rows = await conn.fetch('SELECT * FROM msas ORDER BY $1;', orderby)

        msas = parse_obj_as(list[Msa], [dict(row) for row in rows])

    return ListResponse[Msa](data=msas, total = len(msas), skip = skip, limit = limit)

@router.get("/{msas_id}", response_model=Msa)
async def get_by_id(msas_id: int, pool = Depends(get_db_connection_pool)):
    """Retrieves a msas by ID from the database."""
    async with pool.acquire() as conn:
        row = await conn.fetchrow('SELECT * FROM msas WHERE id = $1;', msas_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'A msa with an id of {msas_id} was not found.')
        msa = parse_obj_as(Msa, dict(row))
    return msa

@router.post("/", response_model=Msa)
async def create_msa(
    title: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    pool = Depends(get_db_connection_pool)
    ):
    """Creates a new msa in the database."""

    # Parse dates
    start_date_parsed = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_parsed = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Create MSA in the database
    async with pool.acquire() as conn:
        row = await conn.fetchrow('''
        INSERT INTO msas (title, start_date, end_date)
        VALUES ($1, $2, $3) RETURNING *;
        ''', title, start_date_parsed, end_date_parsed)

        new_msa = parse_obj_as(Msa, dict(row))
    return new_msa

@router.put("/{msas_id}", response_model=Msa)
async def update_msa(msas_id: int, msa_update: MsaEdit, pool = Depends(get_db_connection_pool)):
    """Updates a msa in the database."""

    msa = await get_by_id(msas_id, pool)
    if msa is None:
        raise HTTPException(status_code=404, detail=f'A msa with an id of {msas_id} was not found.')

    msa.title = msa_update.title
    msa.start_date = msa_update.start_date
    msa.end_date = msa_update.end_date

    async with pool.acquire() as conn:
        row = await conn.fetchrow('''UPDATE msas
        SET title = $1, start_date = $2, end_date = $3
        WHERE id = $4
        RETURNING *;''',
        msa.title, msa.start_date, msa.end_date, msas_id)
        updated_msa = parse_obj_as(Msa, dict(row))
    return updated_msa

@router.delete("/{msas_id}")
async def delete_msas(msas_id: int, pool = Depends(get_db_connection_pool)):
    """Deletes a msa from the database."""
    async with pool.acquire() as conn:
        row = await conn.fetchrow('DELETE FROM msas WHERE id = $1 RETURNING *;', msas_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'A msa with an id of {msas_id} was not found.')
        deleted_vendor = parse_obj_as(Msa, dict(row))
    return deleted_vendor