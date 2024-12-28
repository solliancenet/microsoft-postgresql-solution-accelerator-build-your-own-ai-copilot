from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from sqlalchemy import or_
from data.models import ContractCompany, Vendor


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
