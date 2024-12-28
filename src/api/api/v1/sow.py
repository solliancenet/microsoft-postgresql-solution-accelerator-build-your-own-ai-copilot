from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from data import models, crud
from data.database import SessionLocal, engine

import api.v1.schemas.sows as schemas
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

@router.get("/sows", response_model=ListResponse)
def list_sows(skip: int = 0, limit: int = 10, sortby: str = None, search: str = None, db: Session = Depends(get_db)):
    sows = crud.get_sows(db, skip=skip, limit=limit, sortby=sortby, search=search)
    total = db.query(models.Sow).count()
    sows_pydantic = [schemas.Sow.from_orm(sow) for sow in sows]
    return ListResponse[schemas.Sow](data=sows_pydantic, total=total, skip=skip, limit=limit)

@router.get("/sows/{sow_id}", response_model=schemas.Sow)
def read_sow(sow_id: int, db: Session = Depends(get_db)):
    sow = crud.get_sow(db, sow_id=sow_id)
    if sow is None:
        raise HTTPException(status_code=404, detail="Sow not found")
    return schemas.Sow.from_orm(sow)

# @router.put("/sows/{sow_id}", response_model=schemas.Sow)
# def update_sow(sow_id: int, sow_update: schemas.SowUpdate, db: Session = Depends(get_db)):
#     sow = crud.update_sow(db, sow_id=sow_id, sow_update=sow_update)
#     if sow is None:
#         raise HTTPException(status_code=404, detail="Sow not found")
#     return schemas.Sow.from_orm(sow)