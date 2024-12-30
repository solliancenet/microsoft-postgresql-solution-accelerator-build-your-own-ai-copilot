from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from data import models, crud
from data.database import SessionLocal, engine

import schemas.company as schemas
from schemas.shared import ListResponse

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/company", response_model=ListResponse)
def list_companies(skip: int = 0, limit: int = 10, sortby: str = None, search: str = None, db: Session = Depends(get_db)):
    companies = crud.get_companies(db, skip=skip, limit=limit, sortby=sortby, search=search)
    total = db.query(models.ContractCompany).count()
    data_pydantic = [schemas.ContractCompany.from_orm(company) for company in companies]
    return ListResponse[schemas.ContractCompany](data=data_pydantic, total=total, skip=skip, limit=limit)

@router.get("/company/{company_id}", response_model=schemas.ContractCompany)
def read_company(company_id: int, db: Session = Depends(get_db)):
    company = crud.get_company(db, company_id=company_id)
    if company is None:
        raise HTTPException(status_code=404, detail="Company not found")
    return company