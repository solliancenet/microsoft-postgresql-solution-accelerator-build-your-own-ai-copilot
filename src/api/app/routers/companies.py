from app.lifespan_manager import get_db_connection_pool
from app.models import Company, ListResponse
from fastapi import APIRouter, Depends, HTTPException

# Initialize the router
router = APIRouter(
    prefix = "/companies",
    tags = ["Companies"],
    dependencies = [Depends(get_db_connection_pool)],
    responses = {404: {"description": "Not found"}}
)

@router.get("/", response_model=ListResponse[Company])
async def list_companies(skip: int = 0, limit: int = 10, sortby: str = None, search: str = None, pool = Depends(get_db_connection_pool)):
    """Retrieves a list of companies from the database."""
    async with pool.acquire() as conn:
        orderby = 'id'
        if (sortby):
            orderby = sortby
        print (f'orderby: {orderby}')
        rows = await conn.fetch('SELECT * FROM contract_companies ORDER BY $1 LIMIT $2 OFFSET $3;', orderby, limit, skip)
        companies = [Company(**dict(row)) for row in rows]
    return ListResponse[Company](data=companies, total = len(companies), skip = skip, limit = limit)

@router.get("/{company_id}", response_model=Company)
async def read_company(company_id: int, pool = Depends(get_db_connection_pool)):
    """Retrieves a company by ID from the database."""
    async with pool.acquire() as conn:
        row = await conn.fetchrow('SELECT * FROM contract_companies WHERE id = $1;', company_id)
        if row is None:
            raise HTTPException(status_code=404, detail=f'A company with an id of {company_id} was not found.')
        company = Company(**dict(row))
    return company