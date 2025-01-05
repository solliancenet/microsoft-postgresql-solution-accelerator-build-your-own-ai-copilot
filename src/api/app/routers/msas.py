from app.lifespan_manager import get_db_connection_pool
from app.models import Msa, ListResponse
from fastapi import APIRouter, Depends, HTTPException
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
async def read_msas(msas_id: int, pool = Depends(get_db_connection_pool)):
    """Retrieves a msas by ID from the database."""
    async with pool.acquire() as conn:
        row = await conn.fetchrow('SELECT * FROM msas WHERE id = $1;', msas_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'A msa with an id of {msas_id} was not found.')
        msa = parse_obj_as(Msa, dict(row))
    return msa