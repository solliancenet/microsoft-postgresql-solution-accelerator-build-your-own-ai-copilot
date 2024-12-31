from app.lifespan_manager import get_db_connection_pool
from app.models import Invoice, ListResponse
from fastapi import APIRouter, Depends, HTTPException
import json

# Initialize the router
router = APIRouter(
    prefix = "/invoices",
    tags = ["Invoices"],
    dependencies = [Depends(get_db_connection_pool)],
    responses = {404: {"description": "Not found"}}
)

@router.get("/", response_model=ListResponse[Invoice])
async def list_invoices(skip: int = 0, limit: int = 10, sortby: str = None, search: str = None, pool = Depends(get_db_connection_pool)):
    """Retrieves a list of invoices from the database."""
    async with pool as conn:
        orderby = 'id'
        if (sortby):
            orderby = sortby
        rows = await conn.fetch('SELECT * FROM invoices ORDER BY $1 LIMIT $2 OFFSET $3;', orderby, limit, skip)
        invoices = []
        for row in rows:
            row_dict = dict(row)
            row_dict['invoice_details'] = json.loads(row_dict['invoice_details'])  # Parse JSON string to dictionary
            invoices.append(Invoice(**row_dict))
    return ListResponse(data=invoices, total = len(invoices), skip = skip, limit = limit)

@router.get("/{invoice_id}", response_model=Invoice)
async def read_invoice(invoice_id: int, pool = Depends(get_db_connection_pool)):
    """Retrieves an invoice by ID from the database."""
    async with pool as conn:
        row = await conn.fetchrow('SELECT * FROM invoices WHERE id = $1;', invoice_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'An invoice with an id of {invoice_id} was not found.')
        row_dict = dict(row)
        row_dict['invoice_details'] = json.loads(row_dict['invoice_details'])  # Parse JSON string to dictionary
        invoice = Invoice(**row_dict)
    return invoice