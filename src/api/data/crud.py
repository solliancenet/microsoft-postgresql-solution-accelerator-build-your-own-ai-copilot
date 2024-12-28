from sqlalchemy.orm import Session
from data.models import ContractCompany, Vendor


# ########################################################################################################################
# Company CRUD
# ########################################################################################################################

def get_company(db: Session, company_id: int):
    return db.query(ContractCompany).filter(ContractCompany.id == company_id).first()

def get_companies(db: Session, skip: int = 0, limit: int = 10, sortby: str = None):
    query = db.query(ContractCompany)
    if sortby:
        sort_column, sort_order = sortby.split(':')
        if sort_order == 'desc':
            query = query.order_by(desc(getattr(ContractCompany, sort_column)))
        else:
            query = query.order_by(asc(getattr(ContractCompany, sort_column)))
    return query.offset(skip).limit(limit).all()

# ########################################################################################################################
# Vendor CRUD
# ########################################################################################################################

def get_vendor(db: Session, vendor_id: int):
    return db.query(Vendor).filter(Vendor.id == vendor_id).first()

def get_vendors(db: Session, skip: int = 0, limit: int = 10, sortby: str = None):
    query = db.query(Vendor)
    if sortby:
        sort_column, sort_order = sortby.split(':')
        if sort_order == 'desc':
            query = query.order_by(desc(getattr(Vendor, sort_column)))
        else:
            query = query.order_by(asc(getattr(Vendor, sort_column)))
    return query.offset(skip).limit(limit).all()

