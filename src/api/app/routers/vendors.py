from app.lifespan_manager import get_db_connection_pool
from app.models import Vendor
from fastapi import APIRouter, Depends, HTTPException

# Initialize the router
router = APIRouter(
    prefix = "/vendors",
    tags = ["Vendors"],
    dependencies = [Depends(get_db_connection_pool)],
    responses = {404: {"description": "Not found"}}
)

@router.get('/', response_model = list[Vendor])
async def get(pool = Depends(get_db_connection_pool)):
    """Retrieves a list of vendors from the database."""
    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM vendors;')
        vendors = [Vendor(**dict(row)) for row in rows]
    return vendors

@router.get('/{id:int}', response_model = Vendor)
async def get_by_id(id: int, pool = Depends(get_db_connection_pool)):
    """Retrieves a vendor by ID from the database."""
    async with pool.acquire() as conn:
        row = await conn.fetchrow('SELECT * FROM vendors WHERE id = $1;', id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'A vendor with an id of {id} was not found.')
        vendor = Vendor(**dict(row))
    return vendor

@router.get('/type/{type}', response_model = list[Vendor])
async def get_by_type(type: str, pool = Depends(get_db_connection_pool)):
    """Retrieves vendors of the specified type from the database."""
    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM vendors WHERE LOWER(type) = $1;', type.lower())
        if not rows or len(rows) == 0:
            raise HTTPException(status_code=404, detail=f'No vendors with a type of "{type}" were found.')
        vendors = [Vendor(**dict(row)) for row in rows]
    return vendors