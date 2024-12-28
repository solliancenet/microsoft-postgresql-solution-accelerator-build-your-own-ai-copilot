from sqlalchemy import Column, Integer, String, JSON, Date, Float
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

class Vendor(Base):
    __tablename__ = 'vendors'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    address = Column(String)
    contact_name = Column(String)
    contact_email = Column(String)
    contact_phone = Column(String)
    contact_type = Column("type", String)

class Sow(Base):
    __tablename__ = 'sows'
    id = Column(Integer, primary_key=True, index=True)
    sow_title = Column(String, index=True)
    start_date = Column(Date)
    end_date = Column(Date)
    budget = Column(Float)
    sow_document = Column(String)
    details = Column(JSON)
