from app.lifespan_manager import get_db_connection_pool
from app.models import Deliverable, DeliverableEdit, ListResponse
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Response, Form
from azure.storage.blob import ContentSettings
from datetime import datetime
from pydantic import parse_obj_as

# Initialize the router
router = APIRouter(
    prefix = "/deliverables",
    tags = ["Deliverables"],
    dependencies = [Depends(get_db_connection_pool)],
    responses = {404: {"description": "Not found"}}
)

@router.get("/", response_model=ListResponse[Deliverable])
async def list_deliverables(milestone_id: int = -1, skip: int = 0, limit: int = 10, sortby: str = None, pool = Depends(get_db_connection_pool)):
    """Retrieves a list of deliverables from the database."""
    async with pool.acquire() as conn:
        orderby = 'id'
        if (sortby):
            orderby = sortby

        if limit == -1:
            if milestone_id == -1:
                rows = await conn.fetch('SELECT * FROM deliverables ORDER BY $1;', orderby)
            else:
                rows = await conn.fetch('SELECT * FROM deliverables WHERE milestone_id = $1 ORDER BY $2;', milestone_id, orderby)
        else:
            if milestone_id == -1:
                rows = await conn.fetch('SELECT * FROM deliverables ORDER BY $1 LIMIT $2 OFFSET $3;', orderby, limit, skip)
            else:
                rows = await conn.fetch('SELECT * FROM deliverables WHERE milestone_id = $1 ORDER BY $2 LIMIT $3 OFFSET $4;', milestone_id, orderby, limit, skip)
        
        deliverables = parse_obj_as(list[Deliverable], [dict(row) for row in rows])

        if (milestone_id == -1):
            total = await conn.fetchval('SELECT COUNT(*) FROM deliverables;')
        else:
            total = await conn.fetchval('SELECT COUNT(*) FROM deliverables WHERE milestone_id = $1;', milestone_id)

    if (limit == -1):
        limit = total

    return ListResponse[Deliverable](data=deliverables, total = total, skip = skip, limit = limit)

@router.get("/{deliverable_id}", response_model=Deliverable)
async def get_by_id(deliverable_id: int, pool = Depends(get_db_connection_pool)):
    """Retrieves a deliverable by ID from the database."""
    async with pool.acquire() as conn:
        row = await conn.fetchrow('SELECT * FROM deliverables WHERE id = $1;', deliverable_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'A deliverable with an id of {deliverable_id} was not found.')
        deliverable = parse_obj_as(Deliverable, dict(row))
    return deliverable

@router.post("/", response_model=Deliverable)
async def create_deliverable(
    milestone_id: int = Form(...),
    description: str = Form(...),
    amount: float = Form(None),
    status: str = Form(...),
    due_date: str = Form(None),
    pool = Depends(get_db_connection_pool)
):
    parsed_due_date =  datetime.strptime(due_date, '%Y-%m-%d').date()

    async with pool.acquire() as conn:
        deliverable_id = await conn.fetchval('''
        INSERT INTO deliverables 
        (milestone_id, description, amount, status, due_date) 
        VALUES ($1, $2, $3, $4, $5) RETURNING id;
        ''', milestone_id, description, amount, status, parsed_due_date)
        row = await conn.fetchrow('SELECT * FROM deliverables WHERE id = $1;', deliverable_id)
        deliverable = parse_obj_as(Deliverable, dict(row))
    return deliverable

@router.put("/{deliverable_id}", response_model=Deliverable)
async def update_deliverable(
    deliverable_id: int,
    deliverable: DeliverableEdit,
    pool = Depends(get_db_connection_pool)
):
    async with pool.acquire() as conn:
        # Save the updated deliverable
        await conn.execute('''
        UPDATE deliverables 
        SET description = $1, amount = $2, status = $3, due_date = $4
        WHERE id = $5;
        ''', deliverable.description, deliverable.amount, deliverable.status, deliverable.due_date, deliverable_id)

        row = await conn.fetchrow('SELECT * FROM deliverables WHERE id = $1;', deliverable_id)
        deliverable = parse_obj_as(Deliverable, dict(row))
    return deliverable

@router.delete("/{deliverable_id}")
async def delete_deliverable(deliverable_id: int, pool = Depends(get_db_connection_pool)):
    async with pool.acquire() as conn:
        row = await conn.fetchrow('SELECT * FROM deliverables WHERE id = $1;', deliverable_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'A deliverable with an id of {deliverable_id} was not found.')
        deliverable = parse_obj_as(Deliverable, dict(row))

        await conn.execute('DELETE FROM deliverables WHERE id = $1;', deliverable_id)
    return deliverable
