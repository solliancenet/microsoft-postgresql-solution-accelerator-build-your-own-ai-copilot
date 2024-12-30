from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, Response, Form
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, ContentSettings
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from data import models, crud
from data.database import SessionLocal, engine

import schemas.sows as schemas
from schemas.shared import ListResponse

from config import KeyVaultConfigProvider

config_provider = KeyVaultConfigProvider()

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

@router.post("/sows/create", response_model=schemas.Sow)
def create_sow(
    sow_title: str = Form(...),
    start_date: str = Form(...),
    end_date: str = Form(...),
    budget: float = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Parse dates
    start_date_parsed = datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date_parsed = datetime.strptime(end_date, '%Y-%m-%d').date()

    # Parse budget
    budget_parsed = float(budget)

    # Upload file to Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(config_provider.get_storage_connection_string())
    container_name = config_provider.get_document_container_name()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=file.filename)

    content_settings = ContentSettings(
        content_type=file.content_type,
        content_disposition=f'attachment; filename="{file.filename}"'
    )

    blob_client.upload_blob(file.file, overwrite=True, content_settings=content_settings)

    # Create SOW in the database
    sow_create = schemas.SowEdit(
        sow_title=sow_title,
        start_date=start_date_parsed,
        end_date=end_date_parsed,
        budget=budget_parsed,
        sow_document=file.filename, # Store the filename in the database
        details=None
    )
    sow = crud.create_sow(db=db, sow=sow_create)
    return schemas.Sow.from_orm(sow)

@router.get("/sows/{sow_id}", response_model=schemas.Sow)
def read_sow(sow_id: int, db: Session = Depends(get_db)):
    sow = crud.get_sow(db, sow_id=sow_id)
    if sow is None:
        raise HTTPException(status_code=404, detail="Sow not found")
    return schemas.Sow.from_orm(sow)

@router.put("/sows/{sow_id}", response_model=schemas.Sow)
def update_sow(sow_id: int, sow_update: schemas.SowEdit, db: Session = Depends(get_db)):
    sow = crud.update_sow(db, sow_id=sow_id, sow_update=sow_update)
    if sow is None:
        raise HTTPException(status_code=404, detail="Sow not found")
    return schemas.Sow.from_orm(sow)

@router.delete("/sows/{sow_id}", response_model=schemas.Sow)
def delete_sow(sow_id: int, db: Session = Depends(get_db)):
    sow = crud.delete_sow(db, sow_id=sow_id)
    if sow is None:
        raise HTTPException(status_code=404, detail="Sow not found")
    return schemas.Sow.from_orm(sow)
