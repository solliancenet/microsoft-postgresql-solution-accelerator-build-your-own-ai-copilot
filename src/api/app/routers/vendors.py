from app.lifespan_manager import get_db_connection_pool
from app.models import Vendor, ListResponse
from fastapi import APIRouter, Depends, HTTPException
from pydantic import parse_obj_as

# Initialize the router
router = APIRouter(
    prefix = "/vendors",
    tags = ["Vendors"],
    dependencies = [Depends(get_db_connection_pool)],
    responses = {404: {"description": "Not found"}}
)

@router.get('/', response_model = ListResponse[Vendor])
async def list_vendors(skip: int = 0, limit: int = 10, sortby: str = None, pool = Depends(get_db_connection_pool)):
    """Retrieves a list of vendors from the database."""
    async with pool.acquire() as conn:
        orderby = 'id'
        if (sortby):
            orderby = sortby

        if limit == -1:
            rows = await conn.fetch('SELECT * FROM vendors ORDER BY $1;', orderby)
        else:
            rows = await conn.fetch('SELECT * FROM vendors ORDER BY $1 LIMIT $2 OFFSET $3;', orderby, limit, skip)

        vendors = parse_obj_as(list[Vendor], [dict(row) for row in rows])

        total = await conn.fetchval('SELECT COUNT(*) FROM vendors;')

    if (limit == -1):
        limit = total

    return ListResponse[Vendor](data = vendors, total = len(vendors), skip = 0, limit = len(vendors))

@router.get('/{id:int}', response_model = Vendor)
async def get_by_id(id: int, pool = Depends(get_db_connection_pool)):
    """Retrieves a vendor by ID from the database."""
    async with pool.acquire() as conn:
        row = await conn.fetchrow('SELECT * FROM vendors WHERE id = $1;', id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'A vendor with an id of {id} was not found.')
        vendor = parse_obj_as(Vendor, dict(row))
    return vendor

@router.get('/type/{type}', response_model = list[Vendor])
async def get_by_type(type: str, pool = Depends(get_db_connection_pool)):
    """Retrieves vendors of the specified type from the database."""
    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM vendors WHERE LOWER(type) = $1;', type.lower())
        if not rows or len(rows) == 0:
            raise HTTPException(status_code=404, detail=f'No vendors with a type of "{type}" were found.')
        vendors = parse_obj_as(list[Vendor], [dict(row) for row in rows])
    return vendors
