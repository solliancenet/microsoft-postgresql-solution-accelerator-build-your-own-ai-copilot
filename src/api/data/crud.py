from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from sqlalchemy import or_
from data.models import ContractCompany, Vendor, Sow, Invoice
from schemas.sows import SowEdit

# ########################################################################################################################
# Company CRUD
# ########################################################################################################################

def get_company(db: Session, company_id: int):
    return db.query(ContractCompany).filter(ContractCompany.id == company_id).first()

def get_companies(db: Session, skip: int = 0, limit: int = 10, sortby: str = None, search: str = None):
    query = db.query(ContractCompany)
    
    if search:
        search = f"%{search}%"
        query = query.filter(
            or_(
                ContractCompany.company_name.ilike(search),
                ContractCompany.address.ilike(search),
                ContractCompany.contact_person.ilike(search),
                ContractCompany.contact_email.ilike(search)
            )
        )
    
    if sortby:
        try:
            sort_column, sort_order = sortby.split(':')
            if sort_order == 'desc':
                query = query.order_by(desc(getattr(ContractCompany, sort_column)))
            else:
                query = query.order_by(asc(getattr(ContractCompany, sort_column)))
        except ValueError:
            pass  # Handle the case where sortby is not correctly formatted
    
    return query.offset(skip).limit(limit).all()

# ########################################################################################################################
# Vendor CRUD
# ########################################################################################################################

def get_vendor(db: Session, vendor_id: int):
    return db.query(Vendor).filter(Vendor.id == vendor_id).first()

def get_vendors(db: Session, skip: int = 0, limit: int = 10, sortby: str = None, search: str = None):
    query = db.query(Vendor)
    
    if search:
        search = f"%{search}%"
        query = query.filter(
            or_(
                Vendor.name.ilike(search),
                Vendor.address.ilike(search),
                Vendor.contact_name.ilike(search),
                Vendor.contact_email.ilike(search),
                Vendor.contact_phone.ilike(search),
                Vendor.contact_type.ilike(search)
            )
        )
    
    if sortby:
        try:
            sort_column, sort_order = sortby.split(':')
            if sort_order == 'desc':
                query = query.order_by(desc(getattr(Vendor, sort_column)))
            else:
                query = query.order_by(asc(getattr(Vendor, sort_column)))
        except ValueError:
            pass  # Handle the case where sortby is not correctly formatted
    
    return query.offset(skip).limit(limit).all()

# ########################################################################################################################
# SOW CRUD
# ########################################################################################################################

def get_sow(db: Session, sow_id: int):
    return db.query(Sow).filter(Sow.id == sow_id).first()

def get_sows(db: Session, skip: int = 0, limit: int = 10, sortby: str = None, search: str = None):
    query = db.query(Sow)
    
    if search:
        search = f"%{search}%"
        query = query.filter(
            or_(
                Sow.sow_title.ilike(search),
                Sow.sow_document.ilike(search)
            )
        )
    
    if sortby:
        try:
            sort_column, sort_order = sortby.split(':')
            if sort_order == 'desc':
                query = query.order_by(desc(getattr(Sow, sort_column)))
            else:
                query = query.order_by(asc(getattr(Sow, sort_column)))
        except ValueError:
            pass  # Handle the case where sortby is not correctly formatted
    
    return query.offset(skip).limit(limit).all()

def create_sow(db: Session, sow: SowEdit):
    db_sow = Sow(
        sow_title=sow.sow_title,
        start_date=sow.start_date,
        end_date=sow.end_date,
        budget=sow.budget,
        sow_document=sow.sow_document,
        details=sow.details
    )
    db.add(db_sow)
    db.commit()
    db.refresh(db_sow)
    return db_sow

def update_sow(db: Session, sow_id: int, sow_update: SowEdit):
    db_sow = db.query(Sow).filter(Sow.id == sow_id).first()
    if db_sow:
        db_sow.sow_title = sow_update.sow_title
        db_sow.start_date = sow_update.start_date
        db_sow.end_date = sow_update.end_date
        db_sow.budget = sow_update.budget
        db.commit()
        db.refresh(db_sow)
    return db_sow

def delete_sow(db: Session, sow_id: int):
    db_sow = db.query(Sow).filter(Sow.id == sow_id).first()
    if db_sow:
        db.delete(db_sow)
        db.commit()
    return db_sow

# ########################################################################################################################
# Invoice CRUD
# ########################################################################################################################

def get_invoice(db: Session, invoice_id: int):
    return db.query(Invoice).filter(Invoice.id == invoice_id).first()

def get_invoices(db: Session, skip: int = 0, limit: int = 10, sortby: str = None, search: str = None):
    query = db.query(Invoice)
    
    if search:
        search = f"%{search}%"
        query = query.filter(
            or_(
                Invoice.invoice_number.ilike(search),
                Invoice.payment_status.ilike(search)
            )
        )
    
    if sortby:
        try:
            sort_column, sort_order = sortby.split(':')
            if sort_order == 'desc':
                query = query.order_by(desc(getattr(Invoice, sort_column)))
            else:
                query = query.order_by(asc(getattr(Invoice, sort_column)))
        except ValueError:
            pass  # Handle the case where sortby is not correctly formatted
    
    return query.offset(skip).limit(limit).all()
