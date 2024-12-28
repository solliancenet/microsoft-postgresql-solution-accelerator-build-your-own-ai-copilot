from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from data import models, crud
from data.database import SessionLocal, engine

import api.v1.schemas.invoice as schemas
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

@router.get("/invoices", response_model=ListResponse)
def list_invoices(skip: int = 0, limit: int = 10, sortby: str = None, search: str = None, db: Session = Depends(get_db)):
    invoices = crud.get_invoices(db, skip=skip, limit=limit, sortby=sortby, search=search)
    total = db.query(models.Invoice).count()
    invoices_pydantic = [schemas.Invoice.from_orm(invoice) for invoice in invoices]
    return ListResponse[schemas.Invoice](data=invoices_pydantic, total=total, skip=skip, limit=limit)

@router.get("/invoices/{invoice_id}", response_model=schemas.Invoice)
def read_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = crud.get_invoice(db, invoice_id=invoice_id)
    if invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return schemas.Invoice.from_orm(invoice)