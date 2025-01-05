from app.lifespan_manager import get_db_connection_pool, get_blob_service_client
from app.models import Msa, MsaEdit, ListResponse
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Response, Form
from pydantic import parse_obj_as

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
        rows = await conn.fetch('SELECT * FROM msas ORDER BY $1 LIMIT $2 OFFSET $3;', orderby, limit, skip)
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
    name: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    file: UploadFile = File(...),
    pool = Depends(get_db_connection_pool), blob_service_client = Depends(get_blob_service_client)):
    """Creates a new msa in the database."""

    # Parse dates
    start_date_parsed = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_parsed = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Upload file to Azure Blob Storage
    container_name = appConfig.get_document_container_name()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)

    content_settings = ContentSettings(
        content_type=file.content_type,
        content_disposition=f'attachment; filename="{file.filename}"'
    )

    blob_client.upload_blob(file.file, overwrite=True, content_settings=content_settings)

    # Create MSA in the database
    async with pool.acquire() as conn:
        row = await conn.fetchrow('''
        INSERT INTO msas (msa_title, start_date, end_date, msa_document)
        VALUES ($1, $2, $3, $4) RETURNING *;
        ''', name, start_date_parsed, end_date_parsed, file.filename)

        new_msa = parse_obj_as(Msa, dict(row))
    return new_msa

@router.put("/{msas_id}", response_model=Msa)
async def update_msa(msas_id: int, msa_update: MsaEdit, pool = Depends(get_db_connection_pool)):
    """Updates a msa in the database."""

    msa = await get_by_id(msas_id, pool)
    if msa is None:
        raise HTTPException(status_code=404, detail=f'A msa with an id of {msas_id} was not found.')

    msa.msa_title = msa_update.msa_title
    msa.start_date = msa_update.start_date
    msa.end_date = msa_update.end_date

    async with pool.acquire() as conn:
        row = await conn.fetchrow('''UPDATE msas
        SET msa_title = $1, start_date = $2, end_date = $3
        WHERE id = $4
        RETURNING *;''',
        msa.msa_title, msa.start_date, msa.end_date, msas_id)
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