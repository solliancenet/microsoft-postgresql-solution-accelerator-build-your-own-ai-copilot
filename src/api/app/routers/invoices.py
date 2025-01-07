from app.lifespan_manager import get_db_connection_pool, get_blob_service_client, get_app_config
from app.models import Invoice, InvoiceEdit, ListResponse
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Response, Form
from azure.storage.blob import ContentSettings
from pydantic import parse_obj_as

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
        invoices = parse_obj_as(list[Invoice], [dict(row) for row in rows])
    return ListResponse(data=invoices, total = len(invoices), skip = skip, limit = limit)

@router.get("/{invoice_id}", response_model=Invoice)
async def get_by_id(invoice_id: int, pool = Depends(get_db_connection_pool)):
    """Retrieves an invoice by ID from the database."""
    async with pool as conn:
        row = await conn.fetchrow('SELECT * FROM invoices WHERE id = $1;', invoice_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'An invoice with an id of {invoice_id} was not found.')
        invoice = parse_obj_as(Invoice, dict(row))
    return invoice

@router.post("/", response_model=Invoice)
async def create_invoice(
    number: str = Form(...),
    amount: float = Form(...),
    invoice_date: str = Form(...),
    payment_status: str = Form(...),
    file: UploadFile = File(...),
    pool = Depends(get_db_connection_pool),
    blob_service_client = Depends(get_blob_service_client),
    appConfig = Depends(get_app_config)
    ):
    """Creates a new invoice in the database."""

    # Parse date
    invoice_date_parsed = datetime.strptime(invoice_date, '%Y-%m-%d').date()

    # Upload file to Azure Blob Storage
    container_name = appConfig.get_document_container_name()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)

    content_settings = ContentSettings(
        content_type=file.content_type,
        content_disposition=f'attachment; filename="{file.filename}"'
    )

    blob_client.upload_blob(file.file, overwrite=True, content_settings=content_settings)

    # Create invoice in the database
    async with pool as conn:
        row = await conn.fetchrow('''
        INSERT INTO invoices (number, amount, invoice_date, payment_status, document)
        VALUES ($1, $2, $3, $4, $5) RETURNING *;
        ''', number, amount, invoice_date_parsed, payment_status, file.filename)
        
        new_invoice = parse_obj_as(Invoice, dict(row))
    return new_invoice

@router.put("/{invoice_id}", response_model=Invoice)
async def update_invoice(invoice_id: int, invoice_update: InvoiceEdit, pool = Depends(get_db_connection_pool)):
    """Updates an invoice in the database."""

    invoice = await get_by_id(invoice_id, pool)
    if invoice is None:
        raise HTTPException(status_code=404, detail=f'An invoice with an id of {invoice_id} was not found.')

    invoice.number = invoice_update.number
    invoice.amount = invoice_update.amount
    invoice.invoice_date = invoice_update.invoice_date
    invoice.payment_status = invoice_update.payment_status

    async with pool as conn:
        row = await conn.fetchrow('''
        UPDATE invoices
        SET number = $1, amount = $2, invoice_date = $3, payment_status = $4
        WHERE id = $5
        RETURNING *;
        ''', invoice.number, invoice.amount, invoice.invoice_date, invoice.payment_status, invoice_id)
        
        updated_invoice = parse_obj_as(Invoice, dict(row))
    return updated_invoice

@router.delete("/{invoice_id}", response_model=Invoice)
async def delete_invoice(invoice_id: int, pool = Depends(get_db_connection_pool)):
    """Deletes an invoice from the database."""
    async with pool as conn:
        row = await conn.fetchrow('DELETE FROM invoices WHERE id = $1 RETURNING *;', invoice_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'An invoice with an id of {invoice_id} was not found.')
        deleted_invoice = parse_obj_as(Invoice, dict(row))
    return deleted_invoice
