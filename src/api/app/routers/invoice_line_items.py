from app.lifespan_manager import get_db_connection_pool, get_storage_service, get_azure_doc_intelligence_service
from app.models import InvoiceLineItem, InvoiceLineItemEdit, ListResponse
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Response, Form
from datetime import datetime
from pydantic import parse_obj_as
import json

# Initialize the router
router = APIRouter(
    prefix = "/invoice_line_items",
    tags = ["Invoice Line Items"],
    dependencies = [Depends(get_db_connection_pool)],
    responses = {404: {"description": "Not found"}}
)

@router.get("/", response_model=ListResponse[InvoiceLineItem])
async def list_invoice_line_items(invoice_id: int = -1, skip: int = 0, limit: int = 10, sortby: str = None, pool = Depends(get_db_connection_pool)):
    """Retrieves a list of invoice_line_items from the database."""
    orderby = 'id'
    if (sortby):
        orderby = sortby

    async with pool.acquire() as conn:
        if limit == -1:
            if invoice_id == -1:
                rows = await conn.fetch('SELECT * FROM invoice_line_items ORDER BY $1;', orderby)
            else:
                rows = await conn.fetch('SELECT * FROM invoice_line_items WHERE invoice_id = $1 ORDER BY $2;', invoice_id, orderby)
        else:
            if invoice_id == -1:
                rows = await conn.fetch('SELECT * FROM invoice_line_items ORDER BY $1 LIMIT $2 OFFSET $3;', orderby, limit, skip)
            else:
                rows = await conn.fetch('SELECT * FROM invoice_line_items WHERE invoice_id = $1 ORDER BY $2 LIMIT $3 OFFSET $4;', invoice_id, orderby, limit, skip)

        items = parse_obj_as(list[InvoiceLineItem], [dict(row) for row in rows])

        if (invoice_id == -1):
            total = await conn.fetchval('SELECT COUNT(*) FROM invoice_line_items;')
        else:
            total = await conn.fetchval('SELECT COUNT(*) FROM invoice_line_items WHERE invoice_id = $1;', invoice_id)

    if (limit == -1):
        limit = total

    return ListResponse[InvoiceLineItem](data=items, total = total, skip = skip, limit = limit)

@router.get("/{id}", response_model=InvoiceLineItem)
async def get_by_id(id: int, pool = Depends(get_db_connection_pool)):
    """Retrieves a invoice_line_item by ID from the database."""
    async with pool.acquire() as conn:
        row = await conn.fetchrow('SELECT * FROM invoice_line_items WHERE id = $1;', id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'A invoice_line_item with an id of {id} was not found.')
        item = parse_obj_as(InvoiceLineItem, dict(row))
    return item

@router.post("/", response_model=InvoiceLineItem)
async def create(
    invoice_id: int = Form(...),
    description: str = Form(...),
    amount: float = Form(...),
    status: str = Form(...),
    due_date: str = Form(None),
    pool = Depends(get_db_connection_pool)
):
    # Parse dates
    due_date_parsed = None
    if due_date:
        due_date_parsed = datetime.strptime(due_date, '%Y-%m-%d').date()

    async with pool.acquire() as conn:
        id = await conn.fetchval('''
            INSERT INTO invoice_line_items
            (invoice_id, description, amount, status, due_date)
            VALUES
            ($1, $2, $3, $4, $5)
            RETURNING id;
        ''', invoice_id, description, amount, status, due_date_parsed)
        row = await conn.fetchrow('SELECT * FROM invoice_line_items WHERE id = $1;', id)
        milestone = parse_obj_as(InvoiceLineItem, dict(row))
    return milestone

@router.put("/{id}", response_model=InvoiceLineItem)
async def update(id: int, item: InvoiceLineItemEdit, pool = Depends(get_db_connection_pool)):
    async with pool.acquire() as conn:
        await conn.execute('''
            UPDATE invoice_line_items
            SET invoice_id = $1, description = $2, amount = $3, status = $4, due_date = $5
            WHERE id = $6;
        ''', item.invoice_id, item.description, item.amount, item.status, item.due_date, id)
        row = await conn.fetchrow('SELECT * FROM invoice_line_items WHERE id = $1;', id)
        milestone = parse_obj_as(InvoiceLineItem, dict(row))
    return milestone

@router.delete("/{id}", response_model=InvoiceLineItem)
async def delete(id: int, pool = Depends(get_db_connection_pool)):
    async with pool.acquire() as conn:
        row = await conn.fetchrow('SELECT * FROM invoice_line_items WHERE id = $1;', id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'A invoice_line_item with an id of {id} was not found.')
        await conn.execute('DELETE FROM invoice_line_items WHERE id = $1;', id)
        item = parse_obj_as(InvoiceLineItem, dict(row))
    return item
