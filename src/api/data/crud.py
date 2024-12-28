from sqlalchemy.orm import Session
from data.models import ContractCompany

def get_company(db: Session, company_id: int):
    return db.query(ContractCompany).filter(ContractCompany.id == company_id).first()

def get_companies(db: Session, skip: int = 0, limit: int = 10):
    return db.query(ContractCompany).offset(skip).limit(limit).all()