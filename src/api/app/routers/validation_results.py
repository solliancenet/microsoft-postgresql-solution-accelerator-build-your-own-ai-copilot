from app.lifespan_manager import get_db_connection_pool
from app.models import ListResponse, InvoiceValidationResult, SowValidationResult
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Response, Form
from datetime import datetime
from pydantic import parse_obj_as
import json

# Initialize the router
router = APIRouter(
    prefix = "/validation-results",
    tags = ["Validation Results"],
    dependencies = [Depends(get_db_connection_pool)],
    responses = {404: {"description": "Not found"}}
)

@router.get("/invoice/{id}", response_model=ListResponse[InvoiceValidationResult])
async def list_invoice_validations(id: int, pool = Depends(get_db_connection_pool)):
    """Retrieves a list of validation results for an Invoice from the database."""
    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM invoice_validation_results WHERE invoice_id = $1 ORDER BY datestamp DESC;', id)
        validations = parse_obj_as(list[InvoiceValidationResult], [dict(row) for row in rows])
    return ListResponse(data=validations, total = len(validations), skip = 0, limit = len(validations))


@router.get("/sow/{id}", response_model=ListResponse[SowValidationResult])
async def list_sow_validations(id: int, pool = Depends(get_db_connection_pool)):
    """Retrieves a list of validation results for a SOW from the database."""
    async with pool.acquire() as conn:
        rows = await conn.fetch('SELECT * FROM sow_validation_results WHERE sow_id = $1 ORDER BY datestamp DESC;', id)
        validations = parse_obj_as(list[SowValidationResult], [dict(row) for row in rows])
    return ListResponse(data=validations, total = len(validations), skip = 0, limit = len(validations))
