from app.lifespan_manager import get_db_connection_pool
from app.models import Milestone, MilestoneEdit, ListResponse
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Response, Form
from azure.storage.blob import ContentSettings
from datetime import datetime
from pydantic import parse_obj_as

# Initialize the router
router = APIRouter(
    prefix = "/milestones",
    tags = ["Milestones"],
    dependencies = [Depends(get_db_connection_pool)],
    responses = {404: {"description": "Not found"}}
)

@router.get("/", response_model=ListResponse[Milestone])
async def list_milestones(skip: int = 0, limit: int = 10, sortby: str = None, search: str = None, pool = Depends(get_db_connection_pool)):
    """Retrieves a list of milestones from the database."""
    async with pool.acquire() as conn:
        orderby = 'id'
        if (sortby):
            orderby = sortby
        rows = await conn.fetch('SELECT * FROM milestones ORDER BY $1 LIMIT $2 OFFSET $3;', orderby, limit, skip)
        milestones = parse_obj_as(list[Milestone], [dict(row) for row in rows])

        total = await conn.fetchval('SELECT COUNT(*) FROM milestones;')

    return ListResponse[Milestone](data=milestones, total = total, skip = skip, limit = limit)

@router.get("/{milestone_id}", response_model=Milestone)
async def get_by_id(milestone_id: int, pool = Depends(get_db_connection_pool)):
    """Retrieves a milestone by ID from the database."""
    async with pool.acquire() as conn:
        row = await conn.fetchrow('SELECT * FROM milestones WHERE id = $1;', milestone_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'A milestone with an id of {milestone_id} was not found.')
        milestone = parse_obj_as(Milestone, dict(row))
    return milestone

@router.post("/", response_model=Milestone)
async def create_milestone(
    sow_id: int = Form(...),
    milestone_name: str = Form(...),
    milestone_status: str = Form(...),
    due_date: str = Form(None),
    pool = Depends(get_db_connection_pool)
):
    # Parse dates
    due_date_parsed = None
    if due_date:
        due_date_parsed = datetime.strptime(due_date, '%Y-%m-%d').date()

    async with pool.acquire() as conn:
        milestone_id = await conn.fetchval('INSERT INTO milestones (sow_id, milestone_name, milestone_status, due_date) VALUES ($1, $2, $3, $4) RETURNING id;', sow_id, milestone_name, milestone_status, due_date_parsed)
        row = await conn.fetchrow('SELECT * FROM milestones WHERE id = $1;', milestone_id)
        milestone = parse_obj_as(Milestone, dict(row))
    return milestone

@router.put("/{milestone_id}", response_model=Milestone)
async def update_milestone(
    milestone_id: int,
    sow_id: int = Form(...),
    milestone_name: str = Form(...),
    milestone_status: str = Form(...),
    due_date: str = Form(None),
    pool = Depends(get_db_connection_pool)
):
    # Parse dates
    due_date_parsed = None
    if due_date:
        due_date_parsed = datetime.strptime(due_date, '%Y-%m-%d').date()

    async with pool.acquire() as conn:
        await conn.execute('''
        UPDATE milestones SET sow_id = $1, milestone_name = $2, milestone_status = $3, due_date = $4 
        WHERE id = $5;
        ''', sow_id, milestone_name, milestone_status, due_date_parsed, milestone_id)
        row = await conn.fetchrow('SELECT * FROM milestones WHERE id = $1;', milestone_id)
        milestone = parse_obj_as(Milestone, dict(row))
    return milestone

@router.delete("/{milestone_id}")
async def delete_milestone(milestone_id: int, pool = Depends(get_db_connection_pool)):
    """Deletes a milestone from the database."""
    async with pool.acquire() as conn:
        row = await conn.fetchrow('SELECT * FROM milestones WHERE id = $1 RETURNING *;', milestone_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'A milestone with an id of {milestone_id} was not found.')
        milestone = parse_obj_as(Milestone, dict(row))

        await conn.execute('DELETE FROM milestones WHERE id = $1;', milestone_id)
    return milestone
