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
async def list_vendors(skip: int = 0, limit: int = 10, sortby: str = None, search: str = None, pool = Depends(get_db_connection_pool)):
    """Retrieves a list of vendors from the database."""
    async with pool.acquire() as conn:
        orderby = 'id'
        if (sortby):
            orderby = sortby
        rows = await conn.fetch('SELECT * FROM vendors ORDER BY $1 LIMIT $2 OFFSET $3;', orderby, limit, skip)
        vendors = parse_obj_as(list[Vendor], [dict(row) for row in rows])
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

@router.post('/', response_model = Vendor)
async def create_vendor(vendor: Vendor, pool = Depends(get_db_connection_pool)):
    """Creates a new vendor in the database."""
    async with pool.acquire() as conn:
        row = await conn.fetchrow('INSERT INTO vendors (name, address, contact_name, contact_email, contact_phone, type) VALUES ($1, $2, $3) RETURNING *;', vendor.name, vendor.address, vendor.contact_name, vendor.contact_email, vendor.contact_phone, vendor.type)
        new_vendor = parse_obj_as(Vendor, dict(row))
    return new_vendor

@router.put('/{id:int}', response_model = Vendor)
async def update_vendor(id: int, vendor_update: Vendor, pool = Depends(get_db_connection_pool)):
    """Updates a vendor in the database."""

    vendor = self.get_by_id(id)
    if vendor is None:
        raise HTTPException(status_code=404, detail=f'A vendor with an id of {id} was not found.')

    vendor.name = vendor_update.name
    vendor.address = vendor_update.address
    vendor.contact_name = vendor_update.contact_name
    vendor.contact_email = vendor_update.contact_email
    vendor.contact_phone = vendor_update.contact_phone
    vendor.type = vendor_update.type

    async with pool.acquire() as conn:
        row = await conn.fetchrow('''
        UPDATE vendors
        SET name = $1, address = $2, contact_name = $3, contact_email = $4, contact_phone = $5, type = $6
        WHERE id = $7
        RETURNING *;''',
            vendor.name, vendor.address, vendor.contact_name, vendor.contact_email, vendor.contact_phone, vendor.type, id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'A vendor with an id of {id} was not found.')
        updated_vendor = parse_obj_as(Vendor, dict(row))
    return updated_vendor

@router.delete('/{id:int}', response_model = Vendor)
async def delete_vendor(id: int, pool = Depends(get_db_connection_pool)):
    """Deletes a vendor from the database."""
    async with pool.acquire() as conn:
        row = await conn.fetchrow('DELETE FROM vendors WHERE id = $1 RETURNING *;', id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'A vendor with an id of {id} was not found.')
        deleted_vendor = parse_obj_as(Vendor, dict(row))
    return deleted_vendor