from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class ContractCompany(Base):
    __tablename__ = 'contract_companies'
    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    address = Column(String)
    contact_person = Column(String)
    contact_email = Column(String)
    extra_metadata = Column("metadata", JSON)