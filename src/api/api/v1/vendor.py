from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from data import models, crud
from data.database import SessionLocal, engine

import api.v1.schemas.vendor as schemas
from api.v1.schemas.shared import ListResponse

models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/vendor", response_model=ListResponse)
def list_vendors(skip: int = 0, limit: int = 10, sortby: str = None, db: Session = Depends(get_db)):
    vendors = crud.get_vendors(db, skip=skip, limit=limit, sortby=sortby)
    total = db.query(models.Vendor).count()
    data_pydantic = [schemas.Vendor.from_orm(vendor) for vendor in vendors]
    return ListResponse[schemas.Vendor](data=data_pydantic, total=total, skip=skip, limit=limit)

@router.get("/vendor/{vendor_id}", response_model=schemas.Vendor)
def read_vendor(vendor_id: int, db: Session = Depends(get_db)):
    vendor = crud.get_vendor(db, vendor_id=vendor_id)
    if vendor is None:
        raise HTTPException(status_code=404, detail="Vendor not found")
    return schemas.Vendor.from_orm(vendor)